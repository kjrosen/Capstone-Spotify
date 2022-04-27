'use strict';


// sets event listeners for the constances of the navbar
// item 1/ playlist maker
const maker = document.getElementById('maker');
// item 2/ playlist searcher
const searcher = document.getElementById('searcher');
// reacting to the optional Join navbar item
const joiner = document.getElementById('joiner');
// all forms render to right box
const formBox = document.getElementById('form-box');
// except for login forms those are special snowflakes
const loginBox = document.getElementById('login')
const joinBox = document.getElementById('join')
// all lists render to left box
const listBox = document.getElementById('left-block');
// all playlists render to right box
const embedBox = document.getElementById('embed-box');


// on click a make bar appears in the right bar
maker.addEventListener('click', (evt) => {
	
	let makeInput = '<input type="text" id="new"><br>'
	let makeButt = '<button type="submit">Write</button><br>'
	
	formBox.innerHTML = makeInput+makeButt;
	loginBox.innerHTML = '';
	joinBox.innerHTML = '';
	//on submit create a new event to make the playlist
	//goes to /make and fetches a playlist
	//renders to leftbox
	formBox.addEventListener('submit', (evt) => {
		evt.preventDefault();

		const input = {new: document.getElementById('new').value};

		fetch(`/make.json?${input}`, {
			method: 'POST',
			body: JSON.stringify(input),
			headers: {
				'Content-Type': 'application/json',
			},
		})
			.then(playJson => playJson.text())
			.then(playlistID => {
				listBox.innerHTML = `<iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/${playlistID}?utm_source=generator" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>`
			});
	});
});


// on click a search bar appears in the right bar
searcher.addEventListener('click', (evt) => {
	
	let searchInput = '<input type="text" id="query"><br>'
	let searchButt = '<button type="submit">Search</button><br>'
	
	formBox.innerHTML = searchInput+searchButt
	loginBox.innerHTML = '';
	joinBox.innerHTML = '';
	// on submit create new event
	// goes to /search and returns list of playlists 
	formBox.addEventListener('submit', (evt) => {
		evt.preventDefault();

		const query = {query: document.getElementById('query').value};
		const queryString = new URLSearchParams(query).toString();

		fetch(`/search.json?${queryString}`)
			.then(results => results.json())
			.then(resLists => {

				listBox.innerHTML = ''
				for (const item of resLists) {
					listBox.insertAdjacentHTML('beforeend', `<li id="${item[0]}">${item[1]} by ${item[2]}</li>`);
				}

				// search results and also the most popular all populate in left block
				const plays = document.querySelectorAll('#left-block li');

				for (const play of plays) {
					play.addEventListener('click', (evt) => {
					const playlist = evt.target.id;

					const embed = `<iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/${playlist}?utm_source=generator" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>`
					const likeButt = '<button>Like</button>'

					embedBox.innerHTML = embed+likeButt

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

	const email = '<label>Email: <input type="text" name="email" /></label><br />'
	const pw = '<label>Password: <input type="password" name="password" /></label><br />'
	const name = '<label>Username: <input type="text" name="name" /></label><br />'
	const logbutt = '<button type="submit">Log In</button><br/>'
	const signbutt = '<button type="submit">Sign Up</button>'


	formBox.innerHTML = ''
	loginBox.innerHTML = email+pw+logbutt;
	joinBox.innerHTML = name+email+pw+signbutt;

});


// search results and also the most popular all populate in left block
const plays = document.querySelectorAll('#left-block li');

for (const play of plays) {
	play.addEventListener('click', (evt) => {
		const playlist = evt.target.id;

		const embed = `<iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/${playlist}?utm_source=generator" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>`
		const likeButt = '<button>Like</button>'

		embedBox.innerHTML = embed+likeButt

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