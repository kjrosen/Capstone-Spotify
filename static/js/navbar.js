'use strict';

// sets event listeners for the constances of the navbar
// item 1/ playlist maker
const maker = document.getElementById('maker');
// item 2/ playlist searcher
const searcher = document.getElementById('searcher');
// reacting to the optional Join navbar item
const joiner = document.getElementById('joiner');
// all forms render to right box
// item 1 + 2 + 3/ input box for maker, searcer, joiner
const formBox = document.getElementById('form-box');
// all results from forms render to left box
// search results, made playlist
const listBox = document.getElementById('left-top');
// list results render playlists in the right box
const embedBox = document.getElementById('embed-box');


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

		const input = {new: makeForm.firstChild.value};

		fetch(`/make.json?${input}`, {
			method: 'POST',
			body: JSON.stringify(input),
			headers: {
				'Content-Type': 'application/json',
			},
		})
			.then(playJson => playJson.text())
			.then(playlistID => {
				const bigPlay = embedPlay.cloneNode(true);
				bigPlay.setAttribute('src', `https://open.spotify.com/embed/playlist/${playlistID}?utm_source=generator`);
				listBox.innerHTML = '';
				listBox.appendChild(embedPlay);
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

		const query = {query: seaForm.firstChild.value};
		const queryString = new URLSearchParams(query).toString();
		const results = document.createElement('ul');

		fetch(`/search.json?${queryString}`)
			.then(results => results.json())
			.then(resLists => {

				listBox.innerHTML = '';
				listBox.appendChild(results);
				for (const item of resLists) {
					results.insertAdjacentHTML('beforeend', `<li id="${item[0]}">${item[1]} by ${item[2]}</li>`);
				}

				// search results and also the most popular all populate in left block
				const plays = results.children;

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
									.then(response_ => {
										alert(response_);
									});
						});
					});
				}
			});
	});
});


// on click the input bars appear in Rigt block
//submit goes to either /log_in or /join_up depd on button
joiner.addEventListener('click', (evt) => {
	// TODO: 
	// Passwords are being taken insecurily apparnetly

	const logForm = queryForm.cloneNode(true);
	logForm.setAttribute('action', '/login');
	logForm.setAttribute('method', 'POST');
	logForm.firstChild.setAttribute('type', 'password');
	logForm.firstChild.setAttribute('name', 'password');
	logForm.insertAdjacentHTML('afterbegin', 'Password: ');
	logForm.insertAdjacentElement('afterbegin', inputText.cloneNode(true));
	logForm.firstChild.setAttribute('name', 'email');
	logForm.insertAdjacentHTML('afterbegin', 'Email: ');
	logForm.lastChild.innerText = 'Log In'

	const joinForm = logForm.cloneNode(true);
	joinForm.setAttribute('action', '/join');
	joinForm.insertAdjacentElement('afterbegin', inputText.cloneNode(true));
	joinForm.firstChild.setAttribute('name', 'name');
	joinForm.insertAdjacentHTML('afterbegin', 'Username: ');
	joinForm.lastChild.innerText = 'Sing Up';

	formBox.innerHTML = ''
	formBox.appendChild(logForm);
	formBox.insertAdjacentHTML('beforeend', '<br>');
	formBox.insertAdjacentElement('beforeend', joinForm);

});