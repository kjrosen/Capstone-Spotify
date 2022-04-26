'use strict';


// sets event listeners for the constances of the navbar
// item 1/ playlist maker
const maker = document.getElementById('maker')
// item 2/ playlist searcher
const searcher = document.getElementById('searcher')
// reacting to the optional Join navbar item
const joiner = document.getElementById('joiner')


// on click a make bar appears in the right bar
maker.addEventListener('click', (evt) => {
	const makeBox = document.getElementById('make');
	
	let makeInput = '<input type="text" id="new"><br>'
	let makeButt = '<button type="submit">Write</button><br>'
	
	makeBox.innerHTML = makeInput+makeButt

	//on submit create a new event to make the playlist
	const makeSubmit = document.querySelector('#make button');
	//takes in put from the bar
	//goes to /make and fetches a playlist
	makeSubmit.addEventListener('submit', (eve) => {
		evt.preventDefault();
		const input = {input: document.getElementById('new').value};
		const inputString = new URLSearchParams(input).toString();

		fetch(`/make.json?${inputString}`, {
			method: 'POST',
			body: JSON.stringify(inputString),
			headers: {
				'Content-Type': 'application/json',
			},
		})
			.then(playJson => playJson.text())
			.then(playlistID => {
				const newPlayBox = document.getElementById('left-block');

				newPlayBox.innerHTML = `<iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/${playlistID}?utm_source=generator" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>`
			});
	});
});

// on click a search bar appears in the right bar
searcher.addEventListener('click', (evt) => {
	const searchBox = document.getElementById('search');
	
	let searchInput = '<input type="text" id="query"><br>'
	let searchButt = '<button type="submit">Search</button><br>'
	
	searchBox.innerHTML = searchInput+searchButt

	// on submit create new event
	// takes input from search bar and sends a fetch request
	const seaSubmit = document.querySelector('#search button');
	// goes to /search and returns list of playlists 
	seaSubmit.addEventListener('submit', (evt) => {
		evt.preventDefault();

		const query = {query: document.getElementById('query').value};
		const queryString = new URLSearchParams(query).toString();

		fetch(`/search.json?${queryString}`)
			.then(results => results.json())
			.then(resLists => {

				const box = document.getElementById('left-block');

				box.innerHTML = ''
				for (const item of resLists) {
					box.insertAdjacentHTML('beforeend', `<li id="${item[0]}">${item[1]} by ${item[2]}</li>`);
				}

				// set a nested event listener to make each playlist linkable
				// clicking pulls up full playlist
				const plays = document.querySelectorAll('#left-block li');
				const searchBox = document.getElementById('search-embed');

				for (const play of plays) {
					play.addEventListener('click', (evt) => {
						const playlist = evt.target.id;
						const embed = `<iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/${playlist}?utm_source=generator" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>`
						const ender = '<button>Like</button>'

						searchBox.innerHTML = embed+ender

						// set a nested event listner to like each playlist
						// TODO: adjust the way likes are alerted
						const like = document.querySelector('#search-embed button');

						like.addEventListener('click', (evt) => {
							evt.preventDefault();

							const play = {playlist_id: playlist};

							fetch('/like', {
								method: 'POST',
								body: JSON.stringify(play),
								headers: {
									'Content-Type': 'application/json',
								},
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


// reacts to search bar in base navbar

// on click the input bars appear in Rigt block
//submit goes to either /log_in or /join_up depd on button
joiner.addEventListener('click', (evt) => {
	// TODO: 
	// Passwords are being taken insecurily apparnetly

	const loginBox = document.getElementById('login');
	const signUpBox = document.getElementById('join');

	let email = '<label>Email: <input type="text" name="email" /></label><br />'
	let pw = '<label>Password: <input type="password" name="password" /></label<br />'
	let name = '<label>Username: <input type="text" name="name" /></label><br />'
	let logbutt = '<button type="submit">Log In</button><br/>'
	let signbutt = '<button type="submit">Sign Up</button>'

	loginBox.innerHTML = email+pw+logbutt;
	signUpBox.innerHTML = name+email+pw+signbutt;

});
