'use strict';

// For each element in the navbar that's not a link
// set an event listener

const joiner = document.getElementById('joiner')


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

const searchBox = document.getElementById('search');
   
searchBox.addEventListener('submit', evt => {
    evt.preventDefault();

    const query = {query: document.getElementById('query').value};
    const queryString = new URLSearchParams(query).toString();
    
    fetch(`/search?${queryString}`)
        .then(results => results.json())
        .then(resJson => {
            const box = document.getElementById('left-block')
            box.insertAdjacentHTML('afterbegin', resJson)
        });

});



    


