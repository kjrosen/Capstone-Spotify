'use strict';

// sent event triggers for each item in the navbar, showing new forms or links

// search and make are functionally identical
// below is the html, with spots available for
const form_open = '<form action="'                          //route action
const input_label = '"><label><input type="text" name="'    //input name
const button = '"><br /><button type="submit">'             //button display
const closers = '</button></label></form>'

const bar_ids = [
    ['maker', '/make', 'new', 'Make Playlist'], 
    ['searcher', '/search', 'query', 'Search']
];


// for item 1 the playlist maker, 
// and item 2 the playlist searcher
for (const bar in bar_ids) {
    let id, action, name, butt;
    [id, action, name, butt] = bar

    const targ = document.getElementById(id);

    targ.addEventListener('click', (evt) => {
        box = document.getElementById('pop-bars');
        box.innerHTML = form_open+ action+ input_label+ name+ button+ butt+ closers
    });
}


// (conditional on session info) item 3: log in/sign up
const login = document.getElementById('join');

login.addEventListener('click', (evt) => {
    const box = document.getElementById('pop-bars');

    const login = '<label>Log in'+ form_open+ 'method="POST'+ 

    box.innerHTML = 
    
    
 ><label>Email: <input type="text" name="email" /></label><br /><label>Password: <input type="password" name="password" /></label><br /><button type="submit">Log In</button></form></label><br /><label>Join<form action="/join_up" method="POST"><label>Email: <input type="text" name="email" /></label><br /><label>Password: <input type="password" name="password" /></label><br /><label>Username: <input type="text" name="name" /></label><br /><button type="submit">Sign Up</button></form></label>';

})





// // item 1: new playlist
// const pen = document.getElementById('writer');

// pen.addEventListener('click', (evt) => {
//     const box = document.getElementById('pop-bars');

//     box.innerHTML = '<form action="/make"><label><input type="text" name="new"><br /><button type="submit">Make Playlist</button></label></form>';
// })


// // item 2: search bar
// const search = document.getElementById('search');

// search.addEventListener('click', (evt) => {
//     const box = document.getElementById('pop-bars');

//     box.innerHTML = '<form action="/search"><label><input type="text" name="search"><br /><button type="submit">Search Playlists</button></label></form>';
// })