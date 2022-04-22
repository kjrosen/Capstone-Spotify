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



@app.route('/make', methods=['POST'])
def make_playlsit():
    '''search through the database to fill out the playlist'''

    name = request.form.get('new')
    if session['login'] == False:
        author = ADMIN
    else:
        author = model.User.query.get(session['login'])

    
    playlist = crud.make_playlist(name, author)
    embed = f'https://open.spotify.com/embed/playlist/{playlist}?utm_source=generator" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture'

    return render_template('/show-playlist.html',
                            embed=embed,
                            playlist=playlist)

@app.route('/search.json')
def search_playlists():
    '''search through the db for playlists featuring songs or artists'''

    query = request.args.get('query')
    result = crud.search_db(query)

    return jsonify(result)



@app.route('/like', methods=['POST'])
def like_play():
    '''adds a like between the current user
    and the current playlist'''

    playlist = request.form.get('like')

    # check = crud.make_like(session['login'])

    return redirect('/')



@app.route('/mine')
def show_user_playlists():
    return render_template('my-playlists.html')



# @app.route('/new_playlist')
# def new_playlist():
#     '''this will eventually not render to a new page
#     ideally will be handled by REACT'''
#     return render_template('new_playlist.html')

# @app.route('/search')
# def search():
#     '''this will eventually not render to a new page
#     ideally will be handled by REACT'''
#     return render_template('search.html')

# @app.route('/join')
# def show_sign_in():
#     '''this will eventually not render to a new page
#     ideally will be handled by REACT'''
#     return render_template('join.html')



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
