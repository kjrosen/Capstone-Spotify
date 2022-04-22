'use strict';

// reacting to the optional Join navbar item
const joiner = document.getElementById('joiner')

// on click the input bars appear in Rigt block
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
});//submit goes to either /log_in or /join_up depd on button


// takes input from search bar and sends a fetch request
// goes to /search and returns list of playlists
const searchBox = document.getElementById('search');
   
searchBox.addEventListener('submit', (evt) => {
	evt.preventDefault();

	const query = {query: document.getElementById('query').value};
	const queryString = new URLSearchParams(query).toString();

	fetch(`/search?${queryString}`)
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

			// plays.innerText = "Test";
			for (const play of plays) {
				play.addEventListener('click', (evt) => {
					




				});
			}
		});
});



    


