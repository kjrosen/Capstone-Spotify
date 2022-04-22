'use strict';

// reacting to the optional Join navbar item
const joiner = document.getElementById('joiner')
// on click the input bars appear in Rigt block
//submit goes to either /log_in or /join_up depd on button
joiner.addEventListener('click', (evt) => {
	// TODO: 
	// Passwords are being taken insecurily apparnetly

	const loginBox = document.getElementById('login');
	const signUpBox = document.getElementById('sing-up');

	let email = '<label>Email: <input type="text" name="email" /></label><br />'
	let pw = '<label>Password: <input type="password" name="password" /></label<br />'
	let name = '<label>Username: <input type="text" name="name" /></label><br />'
	let logbutt = '<button type="submit">Log In</button><br/>'
	let signbutt = '<button type="submit">Sign Up</button>'

	loginBox.innerHTML = email+pw+logbutt
	signUpBox.innerHTML = name+email+pw+signbutt
});


// reacts to search bar in base navbar
const searchBox = document.getElementById('search');
// takes input from search bar and sends a fetch request
// goes to /search and returns list of playlists 
searchBox.addEventListener('submit', (evt) => {
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
					searchBox.innerHTML = `<iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/${playlist}?utm_source=generator" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>`
				});
			}
		});
});





// the event that pulls up new playlist creation
//'''''Should this be a route change instead of an event?''''
// const maker = document.getElementById('make')
// // takes input text from the bar and sends a fetch request
// // goes to /make.json and pulls up playlist embed info
// maker.addEventListener('submit', (evt) => {
// 	evt.preventDefault();

// 	const name = {query: document.getElementById('new').value};
// 	const queryString = new URLSearchParams(name).toString();


// });







// window.onSpotifyIframeApiReady = (IFrameAPI) => {
// 	let element = document.getElementById('search-embed');
// 	let options = {
// 		uri: 'spotify:playlist:1rzfBVpG5TrvMITcPpcYC9'
// 	};
// 	let callback = (EmbedController) => {};
// 	IFrameAPI.createController(element, options, callback);
// };
    


