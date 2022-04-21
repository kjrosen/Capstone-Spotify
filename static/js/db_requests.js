'use strict';

// ajax requests sent from navbar.js pop-up menus

// 1: make playlist sends an ajax request and fills Left with new playlist
document.getElementById('make').addEventListener('submit', evt => {
    evt.preventDefault();

    const query = {type: document.getElementById('new').value};

    fetch('/make', {
        method: 'POST',
        body: JSON.stringify(query),
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(rawPlay => rawPlay.json())
        .then(playJson => {

        });
});

// 2: search playlist sends an ajax request and links to 
document.getElementById('search').addEventListener('submit', evt => {
    evt.preventDefault();

    const query = {type: document.getElementById('query').value};

    fetch(`/search?query:${query}`)
        .then(results => results.json())
        .then(resJson => {
            box = document.getElementById('left-block')
            box.insertAdjacentHTML('afterbegin', resJson)
        });
});