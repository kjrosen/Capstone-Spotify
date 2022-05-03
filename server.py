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
    top5 = crud.top5_plays()
    
    # return render_template('home.html')
    return render_template('home.html', top5=top5)



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


@app.route('/verify', methods=['POST'])
def check_user():
    '''checks that the users' information is accurate before changing info'''
    
    ##gets email and password from from
    in_pass = request.json.get('pw')

    ##log in checks database information
    user = model.User.query.get(session['login'])

    if user.pw == in_pass:
        return 'true'


@app.route('/update', methods=['POST'])
def update_user_info():
    '''updates the user's name or password
    emails cannot be updated'''


    new_pw = request.json.get('pw')
    new_name = request.json.get('name')

    user = model.User.query.get(session['login'])

    user.pw = new_pw
    user.name = new_name
    model.db.session.commit()

    flash('Information updated')
    return 'true'



@app.route('/pick.json', methods=['POST'])
def choose_songs():
    '''search through the database to fill out the playlist'''

    name = request.json.get('new')

    songs = crud.find_songs(name)
    
    options = []
    for collection in songs:
        tracks = []
        if len(collection) == 0:
            tracks.append(['standin', 'No options found', 'Gotta spell it out'])
        else:
            for song in collection:
                tracks.append([song.track_id, song.title, song.artist])
        options.append(tracks)

    return jsonify(options)

@app.route('/make.json', methods=['POST'])
def make_playlist():

    if session['login'] == False:
        author = ADMIN
    else:
        author = model.User.query.get(session['login'])
    phrase = request.json.get('phrase')
    tracks = request.json.get('tracks')
    tracks.pop()

    tracklist = crud.fill_chosen_songs(phrase, tracks)
    playlist = crud.make_playlist(phrase, tracklist, author)

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
                            created=playlists['created'],
                            user_name=model.User.query.get(user_id).name)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
