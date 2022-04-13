from flask import Flask, render_template, request, redirect, session
import jinja2
import os

import spotipy


app = Flask(__name__)

app.secret_key = os.environ['SECRET_KEY']

spot_ID = os.environ['SPOT_ID']
spot_SH = os.environ['SPOT_SH']

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/write_new')
def make_playlist():
    return render_template('new_playlist.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/join')
def sign_in():
    return render_template('accounts.html')

@app.route('/my_playlists')
def show_user_playlists():
    return render_template('my_playlists.html')



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
