'use strict';

// prints the navbar, wich each item an event trigger showing new forms or links

// item 1: new playlist
const pen = document.getElementById('writer');

pen.addEventListener('click', (evt) => {
    const box = document.getElementById('pop-bars');

    box.innerHTML = '<form action="/make"><label><input type="text" name="new"><br /><button type="submit">Make Playlist</button></label></form>';
})


// item 2: search bar
const search = document.getElementById('search');

search.addEventListener('click', (evt) => {
    const box = document.getElementById('pop-bars');

    box.innerHTML = '<form action="/search"><label><input type="text" name="search"><br /><button type="submit">Search Playlists</button></label></form>';
})


// (conditional on session info) item 3: log in/sign up
const login = document.getElementById('join');

login.addEventListener('click', (evt) => {
    const box = document.getElementById('pop-bars');

    box.innerHTML = '<label>Log in<form action="/log_in" method="POST"><label>Email: <input type="text" name="email" /></label><br /><label>Password: <input type="password" name="password" /></label><br /><button type="submit">Log In</button></form></label><br /><label>Join<form action="/join_up" method="POST"><label>Email: <input type="text" name="email" /></label><br /><label>Password: <input type="password" name="password" /></label><br /><label>Username: <input type="text" name="name" /></label><br /><button type="submit">Sign Up</button></form></label>';

})