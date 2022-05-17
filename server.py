'''Flask Server for project'''

from flask import Flask, render_template, request, redirect, session, flash, jsonify
import jinja2, os
import crud, model
import time

app = Flask(__name__)
model.connect_to_db(app)

app.secret_key = os.environ['SECRET_KEY']


@app.route('/')
def homepage():
    '''homepage of the app, shows most popular playlists'''

    session['login'] = session.get('login', False)
    top5 = crud.get_top5()
    
    return render_template('home.html', top5=top5)


## account creation based view functions
@app.route('/login', methods=['POST'])
def sign_in():
    '''logs the user in or redirects'''

    in_email = request.form.get('email')
    in_pass = request.form.get('password')

    user_id = crud.log_in(in_email, in_pass)
    
    if user_id == False:
        flash('Wrong password and/or email')
    else:
        session['login'] = user_id
        ##TODO: remember this is still here
        # return redirect('/auth')
    
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
    else:
        session['login'] = user_id
        ##TODO: remember this is here
        # return redirect('/auth')
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
    input_pass = request.json.get('pw')

    ##login checks database information
    user = model.User.query.get(session['login'])

    if user.pw == input_pass:
        return 'true'


@app.route('/update', methods=['POST'])
def update_user_info():
    '''updates the user's name or password
    emails cannot be updated at this time TODO: add extra checks to make emails changable'''

    new_pw = request.json.get('pw')
    new_name = request.json.get('name')

    user = model.User.query.get(session['login'])

    user.pw = new_pw
    user.name = new_name
    model.db.session.commit()

    flash('Information updated')
    return 'true'


## account interaction based view functions
@app.route('/mine')
def show_user_playlists():
    '''fetches the user's liked and created playlists
    sends them to fill the my-playlists page'''

    user_id = session['login']
    playlists = crud.show_user_plays(user_id)
    
    return render_template('my-playlists.html',
                            liked=playlists['liked'],
                            created=playlists['created'],
                            user_name=model.User.query.get(user_id).name)


@app.route('/like', methods=['POST'])
def like_play():
    '''adds a like between the current user
    and the current playlist, and up the playlists' hype'''

    playlist_id = request.json.get('playlist_id')

    response = crud.like_playlist(session['login'], playlist_id)
    
    return response


@app.route('/unlike', methods=['POST'])
def unlike_play():
    '''removes a like between the current user and the current playlist
    lowers the playlist's hype'''

    playlist_id = request.json.get('playlist_id')

    response = crud.unlike_playlist(session['login'], playlist_id)
    
    return response


@app.route('/delete', methods=['POST'])
def delete_playlist():
    '''removes a playlist from the db'''

    playlist_id = request.json.get('playlist_id')

    response = crud.remove_playlist(playlist_id)

    return response

## playlist creation based view functions
@app.route('/pick.json', methods=['POST'])
def choose_songs():
    '''search through the database to fill out the playlist'''

    name = request.json.get('new')

    options = crud.get_tracklist_opts(name)

    return jsonify(options)


@app.route('/make.json', methods=['POST'])
def make_playlist():

    if session['login'] == False:
        author_id = 1
    else:
        author_id = session['login']

    phrase = request.json.get('phrase')
    tracks = request.json.get('tracks')

    tracklist = crud.add_songs_to_tracklist(phrase, tracks)
    playlist = crud.make_spot_playlist(phrase, tracklist, author_id)

    return playlist


## db search based view functions
@app.route('/search.json')
def search_playlists():
    '''search through the db for playlists featuring songs or artists'''

    query = request.args.get('query')
    result = crud.get_play_by_track_keywords(query)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")


