//import two.js to give users something fun to do while waiting for a playlist (it takes a bit)
import Two from 'https://cdn.skypack.dev/two.js@latest';

'use strict';


// sets event listeners for the constances of the navbar
const maker = document.getElementById('maker');
const searcher = document.getElementById('searcher');

// only viewable depending on session data
let joiner = document.querySelectorAll('#joiner');
let adjuster = document.querySelectorAll('#adjuster');

// boxes that results will render into
const formBox = document.getElementById('form-box');
const listBox = document.getElementById('left-top');
const embedBox = document.getElementById('embed-box');
let mainBox = document.querySelectorAll('#mainPlay');


//the basic input form used by both maker and searcher
const queryForm = document.createElement('form');
const inputText = document.createElement('input');
inputText.setAttribute('class', 'input');
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


// for search results always fill on top left list
const results = document.createElement('ul');
results.setAttribute('class', 'container');
results.setAttribute('id', 'seaResults');


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
			embedBox.insertAdjacentHTML('beforeend', '<svg type="button" id="liker" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="#EDA1DB" class="bi bi-heart-fill" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/></svg>');


			// when playlists render to the embed box
			// they become likable
			const like = document.querySelector('#embed-box').lastChild;
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

// for users to play with while their songs are generating
function drawAPicture() {
	//while waiting for songs to be picked, give the user a drawing pad
	//save the drawing made and set as the image of the playlist somehow
	const drawingPad = document.createElement('div');
	listBox.insertAdjacentText('afterbegin', 'Draw a picture while you wait. Click to change colors, double click to stop');
	listBox.insertAdjacentElement('beforeend', drawingPad);
	

	//using a fitted window requires adjusting for the distance between view window and canvas window
	const offset = drawingPad.getBoundingClientRect();

	//an array of colors for the drawing color to cycle through
	const colors = [
		'#00cc00',
		'#0099ff',
		'#cc33ff',
		'#ff0000',
		'#ff9900',
		'#ffff00'
	];

	let colorIndex = 0;

	createGrid();
	
	//create a new Two object, attached to the drawingpad
	let two = new Two({
		type: Two.Types.canvas,
		//TODO: something here is causing a mouse offset, so the lines are appearing about 10px below where the mouse is
		fitted: true,
		autostart: true
	}).appendTo(drawingPad);

	let x, y, line, mouse = new Two.Vector(), randomness = 0;

	//on first click, start the drawing event. end a line with a dblclick 
	drawingPad.addEventListener('mousedown', function(evt) {
		mouse.set(evt.clientX - offset.x, evt.clientY - offset.y);
		line=null;

		drawingPad.addEventListener('mousemove', drag, false);
		drawingPad.addEventListener('mousedown', changeColors, false);
		drawingPad.addEventListener('dblclick', dragEnd, false);
	}, false);

	//all functions for drawing while waiting for playlist - made with two.js

	//creates a line as you drag the mosue
	function drag(evt) {

		x = evt.clientX - offset.x;
		y = evt.clientY - offset.y;

		//if a line doesn't already exist, create it now
		if (!line) {
			const v1 = makePoint(mouse);
			const v2 = makePoint(x, y);
			line = two.makeCurve([v1, v2], true);
			line.noFill().stroke = colors[colorIndex];
			line.linewidth = 10;

			line.vertices.forEach(function(v) {
				v.addSelf(line.translation);
			});
			line.translation.clear();

		} else {
			const v1 = makePoint(x, y);
			line.vertices.push(v1);
		}
		mouse.set(x, y);
	}

	//stops the move event
	function dragEnd(evt) {
		drawingPad.removeEventListener('mousemove', drag, false);
	}

	//makes a new point to connect lines with movement
	function makePoint(x, y) {
		if (arguments.length <= 1) {
			y = x.y;
			x = x.x;
		}

		const v = new Two.Anchor(x, y);
		v.position = new Two.Vector().copy(v);

		return v;
	}

	// creates the canvas to draw on
	function createGrid(s) {
		const size = s || 30;
		let two = new Two({
			type: Two.Types.canvas,
			// fullscreen: true,
			width: size,
			height: size,
		});

		const imageData = two.renderer.domElement.toDataURL('image/png');
		drawingPad.style.backgroundColor = 'white';
		drawingPad.style.backgroundImage = `url(${imageData})`;
		drawingPad.style.backgroundSize = `${size}px`;	
	}

	//cycle through the colors for drawing on click
	function changeColors() {
		colorIndex += 1;
		if (colorIndex > 5){
			colorIndex = 0;
		}
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
			embedBox.insertAdjacentHTML('beforeend', '<svg id="del" type="button" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="#3DB893" class="bi bi-trash3-fill" viewBox="0 0 16 16"><path d="M11 1.5v1h3.5a.5.5 0 0 1 0 1h-.538l-.853 10.66A2 2 0 0 1 11.115 16h-6.23a2 2 0 0 1-1.994-1.84L2.038 3.5H1.5a.5.5 0 0 1 0-1H5v-1A1.5 1.5 0 0 1 6.5 0h3A1.5 1.5 0 0 1 11 1.5Zm-5 0v1h4v-1a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5ZM4.5 5.029l.5 8.5a.5.5 0 1 0 .998-.06l-.5-8.5a.5.5 0 1 0-.998.06Zm6.53-.528a.5.5 0 0 0-.528.47l-.5 8.5a.5.5 0 0 0 .998.058l.5-8.5a.5.5 0 0 0-.47-.528ZM8 4.5a.5.5 0 0 0-.5.5v8.5a.5.5 0 0 0 1 0V5a.5.5 0 0 0-.5-.5Z"/></svg>');
		
			const del = document.querySelector('#embed-box').lastChild;

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
	evt.preventDefault();

	const makeForm = queryForm.cloneNode(true);
	makeForm.lastChild.innerText = 'New';
	formBox.innerHTML = '<label>Name the playlist to get your songs</label>';
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
					track.setAttribute('class', 'row listedPlay');
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
				songPicker.lastChild.setAttribute('id', 'confirm');
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
							
							if (mainBox.length > 0) {
								mainBox = mainBox[0];
								listBox.innerHTML = '';
								mainBox.innerHTML = '';
								mainBox.appendChild(bigPlay);
							} else {
								listBox.innerHTML = '';
								listBox.appendChild(bigPlay);
							}
						});
					
					// //also draw a picture while waiting for playlist to be made
					// drawAPicture();
				});
			});

			//draw a picture while waiting for songs to be picked
			drawAPicture();

	});
});


// on click a search bar appears in the right bar
searcher.addEventListener('click', (evt) => {
	evt.preventDefault();

	const seaForm = queryForm.cloneNode(true);
	seaForm.lastChild.innerText = 'Search';
	formBox.innerHTML = '<label>Search for playlists by tracks</label>';
	formBox.appendChild(seaForm);

	// on submit create new event
	// goes to /search and returns list of playlists 
	seaForm.addEventListener('submit', (evt) => {
		evt.preventDefault();

		listBox.innerHTML = `<h3 class="row">Searching playlists with: ${seaForm.firstChild.value}</h3>`;
		const query = {query: seaForm.firstChild.value};
		const queryString = new URLSearchParams(query).toString();

		fetch(`/search.json?${queryString}`)
			.then(results => results.json())
			.then(resLists => {
				
				results.innerHTML = ''

				if (resLists.length > 0) {
					for (const item of resLists) {
						results.insertAdjacentHTML('beforeend', `<li type="button" class="row listedPlay" id="${item['play id']}">${item['play name']} by ${item['author name']}</li>`);
					}
				} else {
					results.insertAdjacentHTML('beforeend', 'No results');
				}
				
				listBox.appendChild(results);
				listBox.insertAdjacentHTML('afterbegin', '<svg id="exField" type="button" xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="#3DB893" class="bi bi-x-circle-fill" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z"/></svg>');
				const exButton = listBox.firstChild;
				embedListedPlay(results);

				exButton.addEventListener('click', (evt) => {
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
		evt.preventDefault();
		// TODO: 
		// Passwords are being taken insecurily apparnetly
		//the longer forms for log in and sign up
		const logForm = queryForm.cloneNode(true);
		logForm.setAttribute('action', '/login');
		logForm.setAttribute('method', 'POST');
		const passw = logForm.firstChild;
		passw.setAttribute('type', 'password');
		passw.setAttribute('name', 'password');
		logForm.insertAdjacentHTML('afterbegin', '<label>Password: </label>');
		const emai = inputText.cloneNode(true);
		emai.setAttribute('name', 'email');
		emai.setAttribute('type', 'email');
		logForm.insertAdjacentElement('afterbegin', emai);
		logForm.insertAdjacentHTML('afterbegin', '<label>Email: </label>');
		const logButt = logForm.lastChild;
		logButt.innerText = 'Log In';

		const joinForm = logForm.cloneNode(true);
		joinForm.setAttribute('action', '/join');
		joinForm.insertAdjacentElement('afterbegin', inputText.cloneNode(true));
		joinForm.firstChild.setAttribute('name', 'name');
		joinForm.insertAdjacentHTML('afterbegin', '<label>Username: </label>');
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
		evt.preventDefault();

		formBox.innerHTML = '<label>Verify your password:</label>';
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
						formBox.innerHTML = '<lable>Type new name and/or password</label>';
						const change = queryForm.cloneNode(true);
						change.firstChild.setAttribute('type', 'password');
						change.firstChild.setAttribute('id', 'pw');
						change.insertAdjacentHTML('afterbegin', '<label>Password: </label>');
						change.insertAdjacentElement('afterbegin', inputText.cloneNode(true));
						change.firstChild.setAttribute('id', 'name');
						change.insertAdjacentHTML('afterbegin', '<label>Username: </label>');
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
