'''Flask Server for project'''

from flask import Flask, render_template, request, redirect, session, flash, jsonify
import jinja2
import os

import crud
import model


app = Flask(__name__)
model.connect_to_db(app)

app.secret_key = os.environ['SECRET_KEY']
ADMIN = model.User.query.get(1)

@app.route('/')
def homepage():

    session['login'] = session.get('login', False)
    
    return render_template('home.html')



@app.route('/login', methods=['POST'])
def sign_in():
    '''logs the user in or redirects'''

    ##gets email and password from from
    in_email = request.form.get('email')
    in_pass = request.form.get('password')

    ##log in checks database information
    user_id = crud.log_in(in_email, in_pass)

    if user_id == False:
        flash('Wrong password and/or email')
        return redirect('/')
    else:
        session['login'] = user_id
        return redirect('/')

@app.route('/join', methods=['POST'])
def sign_up():
    '''checks user email and creates an account'''

    in_email = request.form.get('email')
    in_pass = request.form.get('password')
    in_name = request.form.get('name')

    user_id = crud.make_account(in_email, in_pass, in_name)

    if user_id == False:
        flash('Email taken')
        return redirect('/')
    else:
        session['login'] = user_id
        return redirect('/')
        
@app.route('/logout')
def logout():
    '''logs a user out'''
    session['login'] = False

    return redirect('/')        



@app.route('/make.json', methods=['POST'])
def make_playlsit():
    '''search through the database to fill out the playlist'''

    name = request.json.get('new')

    if session['login'] == False:
        author = ADMIN
    else:
        author = model.User.query.get(session['login'])

    
    playlist = crud.make_playlist(name, author)

    return playlist

@app.route('/search.json')
def search_playlists():
    '''search through the db for playlists featuring songs or artists'''

    query = request.args.get('query')
    result = crud.search_db(query)

    return jsonify(result)



@app.route('/like', methods=['POST'])
def like_play():
    '''adds a like between the current user
    and the current playlist, and up the playlists' hype'''

    playlist_id = request.json.get('playlist_id')

    response = crud.make_like(session['login'], playlist_id)
    
    return response



@app.route('/mine')
def show_user_playlists():
    '''fetches the user's liked and created playlists
    sends them to fill the my-playlists page'''

    user_id = session['login']
    playlists = crud.show_plays(user_id)
    
    return render_template('my-playlists.html',
                            liked=playlists['liked'],
                            created=playlists['created'])




if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
