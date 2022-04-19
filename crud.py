"""logic/functions/methods for database"""

from model import Track, Feat, Playlist, Likes, User, connect_to_db, db
from random import choice

## imported to crud from server on 4/19
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

##spotipy finds the credentials in the environment and sets it to auth_manager
##for searching and ClientCredentials flow
authorization = SpotifyClientCredentials()
spot = spotipy.Spotify(auth_manager=authorization)
url = 'https://api.spotify.com/v1/search?'
app_id = os.environ['APP_ID']

scope = 'playlist-modify-public'
spot2 = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


'''
# results = spot.search(q='',type='track',limit=50)
songs = results['tracks']['items']
for song in songs:
    song['uri']
    song['name']
    song['artists'][0]['name']

# tracks = spot.playlist_tracks(playlist_id)

# new = spot2.user_playlist_create(app_id, 'play_name')
new playlist redirects to a new page, set it specifically
play more with the redirect and authorization, it's confusing
'''


## below functions create new instances for each table

def create_track(URI, title, artist):
    """take Spotify info and return a new track in local db."""
    
    track = Track(
        uri=URI,
        title=title,
        artist=artist)
    
    return track

def create_feat(track, playlist):
    """Create a connection between track and playlist"""
    
    feat = Feat(
        track_uri=track,
        play_uri=playlist)
    
    return feat

def create_playlist(URI, name, creator):
    """Create and return a new playlist"""

    playlist = Playlist(
        uri=URI, 
        name=name, 
        creator_id=creator)

    return playlist

def create_like(user, playlist):
    """Create a connection between a playlist and a user who didn't author it"""

    like = Likes(
        like_id= str(user)+playlist,
        user_id = user,
        play_id = playlist)

    return like

def create_user(name, email, pw, URI=None):
    """Add a new user to the app"""
    
    user = User(
        uri=URI,
        name=name,
        email=email,
        pw = pw)
    
    return user


## functions for creating an account, logging in, and confirming email isn't taken

def check_email(email):
    '''checks if email is already in db'''

    print()
    print(email)
    check = User.query.filter(User.email==email).all()
    print(check)
    print()

    return (len(check) == 1, check)
    
def log_in(email, password):
    '''checks a user's password, returns true if logged in
    flase if password wrong'''

    user = check_email(email)

    if user[0] == True:

        if user[1][0].pw == password:
            return True
    
    return False

def create_account(email, password, name):
    user = check_email(email)

    if user[0] == False:
        new = create_user(name=name, email=email, pw=password)
        db.session.add(new)
        db.session.commit()
        return True
    else: 
        return False


## functions for creating playlists from user input phrases

def search_tracks_by_title(text):
    '''search for songs from db for each phrase in a text'''

    finds = [text, Track.query.filter(Track.title.like(f'{text} %')).all()]

    return finds


def search_api(word):
    '''performs an api search for the given phrase'''

    result = spot.search(q=word, type='track', limit=50)

    return result


def make_track(results):
    '''goes through set of API search results and turns into tracks'''

    new = []
    for item in results['tracks']['items']:
        if Track.query.get(item['uri']) == None:
            new.append(create_track(
                item['uri'], 
                item['name'], 
                item['artists'][0]['name']))

    db.session.add_all(new)
    db.session.commit()


def find_songs_for_play(phrase):
    '''searches through db, api, on repeat until tracks all found'''
    
    text = phrase.split()

    search = []
    for word in text:
        search.append(search_tracks_by_title(word))

    for result in search:

        queries = 0
        while len(result[1]) == 0:
            new_search = search_api(result[0])
            queries += 1
            make_track(new_search)

            result[1] = search_tracks_by_title(result[0])[1]

            if queries >= 50:
                break

    return search








    



if __name__ == '__main__':
    from server import app
    connect_to_db(app)