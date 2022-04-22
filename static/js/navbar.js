'use strict';

// For each element in the navbar that's not a link
// set an event listener

const maker = document.getElementById('maker')
const searcher = document.getElementById('searcher')
const joiner = document.getElementById('joiner')

const box = document.getElementById('pop-bars');
const out = '<br></input></label>';

// item 1 - the playlist maker
maker.addEventListener('click', (evt) => {

    let label_in = '<label><input type="text" id="make">';
    let button='<br><button type="submit">Write</button>';
    
    box.innerHTML = label_in+button+out;
});

// item 2 - the searcher
searcher.addEventListener('click', (evt) => {

    let label_in = '<label><input type="text" id="search">';
    let button='<br><button type="submit">Search</button>';

    box.innerHTML = label_in+button+out;
})


// (conditional on session info) item 3: log in/sign up
joiner.addEventListener('click', (evt) => {
    // TODO: this looks terrible, make it make it sense
    // I mean it works...
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
   

    


