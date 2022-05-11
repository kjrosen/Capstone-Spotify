'use strict';

// sets event listeners for the constances of the navbar
const maker = document.getElementById('maker');
const searcher = document.getElementById('searcher');
let joiner = document.querySelectorAll('#joiner');

const formBox = document.getElementById('form-box');
const listBox = document.getElementById('left-top');
const embedBox = document.getElementById('embed-box');

let adjuster = document.querySelectorAll('#adjuster');
// let connect = docuement.querySelectorAll('#connect');


//the basic input form used by both maker and searcher
const queryForm = document.createElement('form');
const inputText = document.createElement('input');
inputText.setAttribute('type', 'text');
const button = document.createElement('button');
button.setAttribute('type', 'submit');
queryForm.insertAdjacentElement('beforeend', inputText);
queryForm.insertAdjacentElement('beforeend', button);


//the basic player for embedded playlists
const embedPlay = document.createElement('iframe')
embedPlay.setAttribute('style', 'border-radius:12px');
embedPlay.setAttribute('width', '100%');
embedPlay.setAttribute('height', '380');
embedPlay.setAttribute('frameBorder', '0');
embedPlay.setAttribute('allowfullscreen', '');
embedPlay.setAttribute('allow', 'autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture')


//and X-out options for search results to clear the field
const ex = document.createElement('button');
ex.innerText = 'X'
ex.setAttribute('type', 'button')

// for search results always fill on top left list
const results = document.createElement('ul');
results.setAttribute('class', 'container');


//the feature that lets listed playlists be embedable
// search results and also the most popular all populate in left block
function embedListedPlay(list_box=results) {
	const plays = list_box.children;
	for (const play of plays) {
		play.addEventListener('click', (evt) => {
			const playlist = evt.target.id;
			
			const smallPlay = embedPlay.cloneNode(true);
			smallPlay.setAttribute('src', `https://open.spotify.com/embed/playlist/${ playlist }?utm_source=generator`);
			embedBox.innerHTML = ''
			embedBox.appendChild(smallPlay);
			embedBox.insertAdjacentHTML('beforeend', '<button>Like</button>');

			// when playlists render to the embed box
			// they become likable
			const like = document.querySelector('#embed-box button')
			like.addEventListener('click', (evt) => {
				evt.preventDefault();

				const play = {playlist_id: playlist};
				fetch('/like', {
					method: 'POST',
					body: JSON.stringify(play),
					headers: {
						'Content-Type': 'application/json'},
					})
						.then(response => response.text())
						.then(likeConfirm => {
							// alert(response_);
							if (likeConfirm == 'You already liked this. Unlike?') {
								if (confirm(likeConfirm)) {
									fetch('/unlike', {
										method: 'POST',
										body: JSON.stringify(play),
										headers: {
											'Content-Type': 'application/json'},
										})
										.then(response => response.text())
										.then(unlikeConfirm => {
											alert(unlikeConfirm);
										});
									}
								} else {
									alert(likeConfirm);
								}
						});
			});
		});
	}
}


// on homepage, lists are present in popPlays
const popPlays = document.querySelectorAll('#popular');
if (popPlays.length > 0) {
	embedListedPlay(popPlays[0]);
}


// on myplaylists, lists are already present in authored and liked
const authoredPlays = document.querySelectorAll('#authored');
if (authoredPlays.length > 0) {
	// embedListedPlay(authoredPlays[0]);

	const plays = authoredPlays[0].children;
	for (const play of plays) {
		play.addEventListener('click', (evt) => {
			const playlist = evt.target.id;
			
			const smallPlay = embedPlay.cloneNode(true);
			smallPlay.setAttribute('src', `https://open.spotify.com/embed/playlist/${ playlist }?utm_source=generator`);
			embedBox.innerHTML = ''
			embedBox.appendChild(smallPlay);
			embedBox.insertAdjacentHTML('beforeend', '<button>Delete Playlist</button>');
		
			const del = document.querySelector('#embed-box button');

			del.addEventListener('click', (evt) => {
				evt.preventDefault();

				if (confirm("You can't undo this")){
					const play = {playlist_id: playlist};
					fetch('/delete', {
						method: 'POST',
						body: JSON.stringify(play),
						headers: {
							'Content-Type': 'application/json'},
						})
							.then(response => response.text())
							.then(delResponse => {
								alert(delResponse);
								})
					}
			});
		});
	}
}


// use embedListedPlay if they exist
const likedPlays = document.querySelectorAll('#liked');
if (likedPlays.length > 0) {
	embedListedPlay(likedPlays[0]);
}


// on click a make bar appears in the right bar
maker.addEventListener('click', (evt) => {
	
	const makeForm = queryForm.cloneNode(true);
	makeForm.lastChild.innerText = 'New';
	formBox.innerHTML = '';
	formBox.appendChild(makeForm);

	//on submit create a new event to make the playlist
	//goes to /make and fetches a playlist
	//renders to leftbox
	makeForm.addEventListener('submit', (evt) => {
		evt.preventDefault();

		const playName =  makeForm.firstChild.value
		const input = {new: playName};

		fetch(`/pick.json?${input}`, {
			method: 'POST',
			body: JSON.stringify(input),
			headers: {
				'Content-Type': 'application/json',
			},
		})
		  .then(songJson => songJson.json())
			.then(listedSongs => {
				
				listBox.innerHTML = '<h3 class="row">Pick Your Songs<h3>';
				const songPicker = document.createElement('form');
				songPicker.setAttribute('class', 'container');
				const skip = document.createElement('option');
				skip.setAttribute('value', 'skip');
				skip.innerText = 'Skip this song';
				const spell = document.createElement('option');
				spell.setAttribute('value', 'standin');
				spell.innerText = 'Spell it out instead';


				// create a drop down menu for each song choice
				for (const query of listedSongs) {
					const track = document.createElement('select');
					track.setAttribute('class', 'row');
          			track.appendChild(skip.cloneNode(true));
					track.appendChild(spell.cloneNode(true));
					songPicker.appendChild(track);

					for (const opt of query) {
						const option = document.createElement('option');
						option.setAttribute('value', opt['track_id']);
						option.innerText = `${ opt['song title']} by ${ opt['song artist'] }`;
						songPicker.lastChild.appendChild(option);
					}
				}

				songPicker.appendChild(button.cloneNode(true));
				songPicker.removeAttribute('class');
				songPicker.lastChild.innerText = 'Confirm';

				listBox.appendChild(songPicker);

				// take the ids of choices back to server
				// to make a playlist
				songPicker.addEventListener('submit', (evt) => {
					evt.preventDefault();

					const chosen = [];
					for (const opt of songPicker.children) {
						chosen.push(opt.value);
					}
					
					const playInfo = {
						phrase: playName,
						tracks: chosen,
					}

					fetch('/make.json', {
						method: 'POST',
						body: JSON.stringify(playInfo),
						headers: {
							'Content-Type': 'application/json',
						},
					})
						.then(playJson => playJson.text())
						.then(playlistID => {
							const bigPlay = embedPlay.cloneNode(true);
							bigPlay.setAttribute('src', `https://open.spotify.com/embed/playlist/${playlistID}?utm_source=generator`);
							listBox.innerHTML = '';
							listBox.appendChild(bigPlay);
						});
				});
			});
	});
});


// on click a search bar appears in the right bar
searcher.addEventListener('click', (evt) => {
	
	const seaForm = queryForm.cloneNode(true);
	seaForm.lastChild.innerText = 'Search';
	formBox.innerHTML = '';
	formBox.appendChild(seaForm);

	// on submit create new event
	// goes to /search and returns list of playlists 
	seaForm.addEventListener('submit', (evt) => {
		evt.preventDefault();

		listBox.innerHTML = '';
		const query = {query: seaForm.firstChild.value};
		const queryString = new URLSearchParams(query).toString();

		fetch(`/search.json?${queryString}`)
			.then(results => results.json())
			.then(resLists => {
				
				listBox.innerHTML = `<h3 col="row">${queryString}</h3>`;
				results.innerHTML = ''

				if (resLists.length > 0) {
					for (const item of resLists) {
						results.insertAdjacentHTML('beforeend', `<li class="row" id="${item['play id']}">${item['play name']} by ${item['author name']}</li>`);
					}
				} else {
					results.insertAdjacentHTML('beforeend', 'No results');
				}
				
				listBox.appendChild(results);
				listBox.insertAdjacentElement('afterbegin', ex);
				embedListedPlay(results);

				ex.addEventListener('click', (evt) => {
					evt.preventDefault();
					listBox.innerHTML = '';
				});
			});
	});
});


// on click the input bars appear in Rigt block
//submit goes to either /log_in or /join_up depd on button
if (joiner.length > 0) {
	joiner = joiner[0];
	joiner.addEventListener('click', (evt) => {
		// TODO: 
		// Passwords are being taken insecurily apparnetly
		//the longer forms for log in and sign up
		const logForm = queryForm.cloneNode(true);
		logForm.setAttribute('action', '/login');
		logForm.setAttribute('method', 'POST');
		const passw = logForm.firstChild;
		passw.setAttribute('type', 'password');
		passw.setAttribute('name', 'password');
		logForm.insertAdjacentHTML('afterbegin', '<br>Password: <br>');
		const emai = inputText.cloneNode(true);
		emai.setAttribute('name', 'email');
		logForm.insertAdjacentElement('afterbegin', emai);
		logForm.insertAdjacentHTML('afterbegin', '<br>Email: <br>');
		const logButt = logForm.lastChild;
		logButt.innerText = 'Log In';

		const joinForm = logForm.cloneNode(true);
		joinForm.setAttribute('action', '/join');
		joinForm.insertAdjacentElement('afterbegin', inputText.cloneNode(true));
		joinForm.firstChild.setAttribute('name', 'name');
		joinForm.insertAdjacentHTML('afterbegin', '<br>Username: <br>');
		joinForm.lastChild.innerText = 'Sing Up';

		formBox.innerHTML = '';
		formBox.appendChild(logForm);
		formBox.insertAdjacentHTML('beforeend', '<br>');
		formBox.insertAdjacentElement('beforeend', joinForm);
	
	});
}


// if the user is already logged in they can adjust their name or password
if (adjuster.length > 0){
	adjuster = adjuster[0];

	adjuster.addEventListener('click', (evt) => {
		formBox.innerHTML = 'Verify your password<br>';
		const verify = queryForm.cloneNode(true);
		verify.firstChild.setAttribute('type', 'password');
		verify.lastChild.innerText = 'Confirm'
		formBox.appendChild(verify);

		verify.addEventListener('submit', (evt) => {
			evt.preventDefault();
			
			const verifyForm = {
				pw: verify.firstChild.value,
			};

			fetch('/verify', {
				method: 'POST',
				body: JSON.stringify(verifyForm),
				headers: {
					'Content-Type': 'application/json',
				},
			})
				.then(response => response.text())
				.then(confirmation => {
					if (confirmation == 'true') {
						formBox.innerHTML = 'Type new name and/or password<br>';
						const change = queryForm.cloneNode(true);
						change.firstChild.setAttribute('type', 'password');
						change.firstChild.setAttribute('id', 'pw');
						change.insertAdjacentHTML('afterbegin', 'Password: <br>');
						change.insertAdjacentElement('afterbegin', inputText.cloneNode(true));
						change.firstChild.setAttribute('id', 'name');
						change.insertAdjacentHTML('afterbegin', 'Username: <br>');
						change.lastChild.innerText = 'Update';
						formBox.appendChild(change);

						change.addEventListener('submit', (evt) => {
							evt.preventDefault()

							const updateInfo = {
								name: document.getElementById('name').value,
								pw: document.getElementById('pw').value,
							}

							fetch('/update', {
								method: 'POST',
								body: JSON.stringify(updateInfo),
								headers: {
									'Content-Type': 'application/json',
								},
							})
								.then(response => response.text())
								.then(confirm => {
									if (confirm == 'true') {
									location.reload();
									}
								});
						});
					} else {
						alert("Wrong password")
					}
				});
		});
	});
}



