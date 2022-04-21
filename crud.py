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

def create_playlist(URI, name, creator, hype=0):
    """Create and return a new playlist"""

    playlist = Playlist(
        uri=URI, 
        name=name, 
        creator_id=creator,
        hype=hype)

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
    '''checks if email is already in db, returns query search'''

    check = User.query.filter(User.email==email).all()

    return check
    
def log_in(email, password):
    '''checks a user's password, returns their id if successful
    flase if password wrong or email not in db'''

    user = check_email(email)

    if len(user) == 1:
        user = user[0]

        if user.pw == password:
            return user.user_id
    
    return False

def make_account(email, password, name):
    '''checks if user email is taken
    if not, creates an account
    returns new users' id
    
    returns false if email is taken'''

    if len(check_email(email)) == 0:
        new = create_user(name=name, email=email, pw=password)
        db.session.add(new)
        db.session.commit()
        return new.user_id
    else: 
        return False


## functions for creating playlists from user input phrases
def make_search_options(phrase):
    '''make many options for each word in the phrase to use for SQL searches
    look for upper.(), title.(), lower() of each word
    then those options followed by different punctuation
    then abbreviations for each version
    then each word plus the one after it, and the one after that
    then each word plus one before, and one before that
    then each word plus one before and one after'''

def search_tracks_by_title(text):
    '''search for songs from db for each phrase in a text'''

    upper = text.upper()
    title = text.title()
    lower = text.lower()
    options = [upper, title, lower]
    '''replace with the make_search_options from above'''

    finds = [text, []]
    for opt in options:
        search = Track.query.filter(Track.title.like(f'{opt} %')).all()
        for item in search:
            finds[1].append(item)

    return finds

def search_api(word, offset=0):
    '''performs an api search for the given phrase'''

    result = spot.search(q=word, type='track', limit=50, offset=offset)

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

    '''impliment the make_search_options function once it's completed'''
    search = []
    for word in text:
        search.append(search_tracks_by_title(word))

    for result in search:

        queries = 0
        while len(result[1]) == 0:
            new_search = search_api(result[0], queries)
            queries += 1
            make_track(new_search)

            result[1] = search_tracks_by_title(result[0])[1]

            if queries > 10:
                break

    return search

def pick_songs(playlists):
    '''pick a random option from the results to pick for playlist'''

    picks = []
    for keyword in playlists:
        if len(keyword[1]) > 0:
            picks.append(choice(keyword[1]))

    return picks

def make_playlist(phrase, creator=1):
    '''takes in a given phrase and makes a spotify playlist full of songs
    currently the first word from title spells out the word
    
    TODO: change to closer title matches'''

    new = spot2.user_playlist_create(app_id, phrase)

    options = find_songs_for_play(phrase)
    final = pick_songs(options)

    ids = []
    for song in final:
        ids.append(song.uri)

    spot.playlist_add_items(new['id'], ids)

    playlist = create_playlist(new['uri'], phrase, creator)

    db.session.add(playlist)
    db.session.commit()




    



if __name__ == '__main__':
    from server import app
    connect_to_db(app)