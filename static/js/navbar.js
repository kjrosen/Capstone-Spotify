'use strict';

// sets eventListners for each item in the navbar

// for item 1 the playlist maker and item 2 the playlist searcher

// search and make are functionally identical
// below is the html, with spots available for
const form_open = '<form id="'                          //route action
const input_label = '"><label><input type="text" name="'    //input name
const button = '"><br /><button type="submit">'             //button display
const closers = '</button></label></form>'
const bar_ids = [
    ['maker', 'make', 'new', 'Make Playlist'], 
    ['searcher', 'search', 'query', 'Search']
];

for (const bar of bar_ids) {
    const id = bar[0];
    const action = bar[1];
    const name = bar[2];
    const butt = bar[3];

    const targ = document.getElementById(id);

    targ.addEventListener('click', (evt) => {
        const box = document.getElementById('pop-bars');
        box.innerHTML = form_open+ action+ input_label+ name+ button+ butt+ closers
    });
}


// (conditional on session info) item 3: log in/sign up
const login = document.getElementById('join');

login.addEventListener('click', (evt) => {
    // TODO: this looks terrible, make it make it sense
    // I mean it works...
    // Passwords are being taken insecurily apparnetly

    const box = document.getElementById('pop-bars');

    const email = '" method="POST"><label>Email: <input type="text" name="email" /></label><br />'
    const pass = '<label>Password: <input type="password" name="password" /></label><br />'
    const logbutt = '<label><button type="submit">Log in</button></label></form></label>'

    const user = '<label>Nickname: <input type="text" name="name" /></label><br />'
    const signbut = '<label><button type="submit">Join Up</button></label></form></label>'

    const login = '<label>Log in<br />'+ form_open+ '/log_in" method="POST"'+ email+ pass+ logbutt
    const signup = '<label>Join<br />'+ form_open+ '/join_up" method="POST"'+ email+ pass+ user+ signbut

    box.innerHTML = login +'<br />'+ signup
});
