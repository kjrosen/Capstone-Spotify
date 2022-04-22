'''Flask Server for project'''

from flask import Flask, render_template, request, redirect, session, flash, jsonify
import jinja2
import os

import crud
import model


app = Flask(__name__)
model.connect_to_db(app)

app.secret_key = os.environ['SECRET_KEY']


@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/log_in', methods=['POST'])
def sign_in():
    '''logs the user in or redirects'''

    ##gets email and password from from
    in_email = request.form.get('email')
    in_pass = request.form.get('password')

    ##log in checks database information
    user = crud.log_in(in_email, in_pass)

    if user == False:
        flash('Wrong password and/or email')
        return redirect('/')
    else:
        session['login'] = user
        return redirect('/my_playlists')

@app.route('/join_up', methods=['POST'])
def sign_up():
    '''checks user email and creates an account'''

    in_email = request.form.get('email')
    in_pass = request.form.get('password')
    in_name = request.form.get('name')

    user = crud.make_account(in_email, in_pass, in_name)

    if user == False:
        flash('Email taken')
        return redirect('/')
    else:
        session['login'] = user
        return redirect('/my_playlists')
        
@app.route('/logout')
def logout():
    '''logs a user out'''
    session['login'] = False

    return redirect('/')        



@app.route('/make')
def make_playlsit():
    '''search through the database to fill out the playlist'''

    # name = request.form.get('new')
    
    # playlist = crud.make_playlist(name)

    return render_template('/new_playlist')



@app.route('/search')
def search_playlists():
    '''search through the db for playlists featuring songs or artists'''

    query = request.args.get('query')
    result = crud.search_db(query)

    return jsonify(result)


@app.route('/my_playlists')
def show_user_playlists():
    return render_template('my_playlists.html')



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
