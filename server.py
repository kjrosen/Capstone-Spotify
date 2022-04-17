'''Flask Server for project'''

from flask import Flask, render_template, request, redirect, session
import jinja2
import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

##spotipy finds the credentials in the environment and sets it to auth_manager
authorization = SpotifyClientCredentials()
spot = spotipy.Spotify(auth_manager=authorization)
url = 'https://api.spotify.com/v1/search?'

app = Flask(__name__)

app.secret_key = os.environ['SECRET_KEY']


# results = spot.search(q='',type='track',limit=50)
'''relevant info is results['tracks']['items']
will result in a list full of libraries

songs = results['tracks']['items']
will want song['name'] for checks
and song['uri'] for further fetching
song['artists'][0]['name'] to get primary artist name'''



@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/write_new')
def make_playlist():
    '''this will eventually not render to a new page
    ideally will be handled by REACT'''
    return render_template('new_playlist.html')

@app.route('/search')
def search():
    '''this will eventually not render to a new page
    ideally will be handled by REACT'''
    return render_template('search.html')

@app.route('/join')
def sign_in():
    '''this will eventually not render to a new page
    ideally will be handled by REACT'''
    return render_template('accounts.html')

@app.route('/my_playlists')
def show_user_playlists():
    return render_template('my_playlists.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
