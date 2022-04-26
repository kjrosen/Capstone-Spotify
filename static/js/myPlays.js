'use strict';

const plays = document.querySelectorAll('#left-block li');
const searchBox = document.getElementById('search-embed');

for (const play of plays) {
    play.addEventListener('click', (evt) => {
        const playlist = evt.target.id;

        const embed = `<iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/${playlist}?utm_source=generator" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>`

        searchBox.innerHTML = embed
    });
}



