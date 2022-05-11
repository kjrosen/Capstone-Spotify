"""logic/functions/methods for database"""

from model import Track, Feat, Playlist, Likes, User, connect_to_db, db
from random import choice
import search_helpers

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
auth = SpotifyOAuth(scope=scope)
spot_user = spotipy.Spotify(auth_manager=auth)


'''## functions to create new instances for each table'''
def create_track(track_id, title, artist):
    """take Spotify info and return a new track in local db."""
    
    track = Track(
        track_id=track_id,
        title=title,
        artist=artist)
    
    return track

def create_feat(track_id, playlist_id):
    """Create a connection between track and playlist"""
    
    feat = Feat(
        track_id=track_id,
        play_id=playlist_id)
    
    return feat

def create_playlist(play_id, name, creator_id, hype=0):
    """Create and return a new playlist"""

    playlist = Playlist(
        play_id=play_id, 
        name=name, 
        creator_id=creator_id,
        hype=hype)

    return playlist

def create_like(user_id, playlist_id):
    """Create a connection between a playlist and a user who didn't author it"""

    like = Likes(
        like_id= str(user_id)+playlist_id,
        user_id = user_id,
        play_id = playlist_id)

    return like

def create_user(name, email, pw, spot_id=None):
    """Add a new user to the app"""
    
    user = User(
        spot_id=spot_id,
        name=name,
        email=email,
        pw = pw)
    
    return user


'''## functions for creating an account management'''
def check_email(email):
    '''checks if email is already in db, returns list of user exists '''

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


'''## functions for creating playlists from user input phrases'''
def get_tracks_by_title(queries):
    '''search for songs from db for the given set of search parameters phrase in a text'''

    search = Track.query.filter(Track.title.in_(queries)).all()

    return search


def get_tracks_with_multi_artists(queries):
    '''search for songs that allow for featured artist'''

    search = []

    for query in queries:
        search += Track.query.filter(
            (Track.title.like(f'{query} (feat.%')) | 
            (Track.title.like(f'{query} (with%)')) | 
            (Track.title.like(f'{query} (Featuring%')) |
            (Track.title.like(f'{query} (Feat.%')) |
            (Track.title.like(f'{query} (With%'))
            ).all()
    
    return search


def search_api(word, offset=0):
    '''performs an api search for the given phrase'''

    result = spot.search(q=word, type='track', limit=50, offset=offset)

    return result


def make_tracks(results):
    '''goes through set of API search results and turns into track objects'''

    new = []
    for item in results['tracks']['items']:
        if Track.query.get(item['id']) == None:
            new.append(create_track(
                item['id'], 
                item['name'], 
                item['artists'][0]['name']))

    db.session.add_all(new)
    db.session.commit()


def get_songs_by_search_list(query):
    '''takes a list of search terms and searches through db, then api, on repeat until at least one option is found
    stops after 10 api searches to cut back on wait time and call number 
    and because 500 is a lot of songs to result in nothing'''

    search = get_tracks_by_title(query)

    q_num = 0
    while len(search) == 0 and q_num < 10:
        new_search = search_api(query[0], q_num)
        new = make_tracks(new_search)
        search += get_tracks_by_title(query)
        search += get_tracks_with_multi_artists(query)
        q_num += 1


    return search


def get_tracklist_opts(phrase):
    '''creates a dictionary of search options for each word in a phrase
    finds songs for each set of search options'''
    
    query_dict = search_helpers.make_search_options(phrase)
        
    options = []

    for query in query_dict:
        song_opts = get_songs_by_search_list(query_dict[query])
        # query_dict[query].append(songs_opts)

        tracklist = []
        if len(song_opts) == 0:
            pass
        else:
            for song in song_opts:
                tracklist.append({'track_id': song.track_id, 'song title': song.title, 'song artist': song.artist})
        options.append(tracklist)

    return options


def get_songs_to_spell_word(word):
    '''search through db and api for songs with single letter or phonetic titles that spell out a given word'''

    acronym = []

    word = search_helpers.remove_punctuation(word)
    word = word.lower()
    for lett in word:
        if lett == "c":
            char = 'seed'
        elif lett == "l":
            char = 'elle'
        elif lett == "p":
            char = 'pea'
        elif lett == "t":
            char = 'tea'
        else:
            char = lett

        print('\n\n\n\n\n\n\n', char)
        char_choice = []
        ## create a collection of search options just like for a regular word    
        char_choice.append(char)
        char_choice.append(char.upper())
        char_choice.append(char.title())
        char_choice += search_helpers.adds_punctuation(char) 
        char_choice += search_helpers.adds_punctuation(char.upper())
        char_choice += search_helpers.adds_punctuation(char.title())
        
        opts = get_songs_by_search_list(char_choice)

        if len(opts) > 1:
            acronym.append(choice(opts))

    return acronym


def add_songs_to_tracklist(phrase, tracks):
    '''takes the input phrase, the tracks chosen by the user, adds songs to tracklist
    if user neglected to pick, it skips, if they wanted it spelled, find acronyms
    '''

    track_list = []
    words = phrase.split()
    i = 0

    ## there are always exactly as many tracks selected as words in the phrase, by design
    ## user may have chosen a song, to spell it out, or to skip entirely
    for word in words:
        if tracks[i] == 'standin':
            acronym = get_songs_to_spell_word(word)
            for song in acronym:
                track_list.append(song)
        elif tracks[i] == 'skip':
            pass
        else: 
            track_list.append(Track.query.get(tracks[i]))
        i += 1

    return track_list


def make_spot_playlist(phrase, tracks, author_id):
    '''takes in a given phrase and makes a spotify playlist full of songs

    returns the playlist id for embedding
    '''
  
    ## cannot give spotify ownership to users - TODO:
    ## figure out how to give it to them

    new = spot_user.user_playlist_create(app_id, phrase)

    playlist = create_playlist(new['id'], phrase, author_id)

    play_fs = [playlist]
    for track in tracks:
        spot_user.playlist_add_items(new['id'], [track.track_id])
        feat = create_feat(track.track_id, playlist.play_id)
        play_fs.append(feat)

    db.session.add_all(play_fs)
    db.session.commit()

    return playlist.play_id


'''## functions for user interaction'''
def get_play_by_track_keywords(query):
    '''searches through db for query keywords'''

    play_q = db.session.query(Playlist)
    join_feat = play_q.join(Feat, Playlist.play_id==Feat.play_id)
    play_feat_track = join_feat.join(Track, Track.track_id==Feat.track_id)
    where = play_feat_track.filter(
        (Track.title.like(f'%{query}%')) | (Track.artist.like(f'%{query}%')) | (Track.title.like(f'%{query.lower()}%'))
        | (Track.artist.like(f'%{query.lower()}%')) | (Track.title.like(f'%{query.title()}%')) | 
        (Track.artist.like(f'%{query.title()}%')))
    
    results = where.all()
    show = []

    if len(results) > 0:
        for item in results:
            author = User.query.get(item.creator_id)
            show.append({'play id': item.play_id, 'play name': item.name, 'author name': author.name})

    return show


def get_top5():
    '''queries database for current 5 most liked playlists
    returns the id, name, author name, and hype score for each in a list of dicts'''

    playlists = db.session.query(Playlist).order_by('hype').all()

    top5 = []
    for play in playlists[-1:-6:-1]:
        top5.append({'play id': play.play_id, 'play name': play.name, 'author name': play.author.name, 'hype': play.hype})

    return top5


def like_playlist(user_id, playlist_id):
    '''checks that the user didn't author the playlist
    checks that the user hasn't already liked the playlist
    checks that the user is logged in
    
    if all pass creates a like instance
    return success message
    or specific failure message
    '''
    playlist = Playlist.query.get(playlist_id)

    if user_id == False:
        return("You need to be logged in to like")
    else:
        if playlist.creator_id == user_id:
            return "You made this playlist"
        else:
            if Likes.query.get(str(user_id)+str(playlist_id)):
                return "You already liked this. Unlike?"
            else:
                like = create_like(user_id, playlist_id)
                db.session.add(like)
                playlist.hype += 1
                db.session.commit()
                return "Liked!"

def unlike_playlist(user_id, playlist_id):
    '''deletes a like item from the db
    lowers the playlist's hype score as well'''

    playlist = Playlist.query.get(playlist_id)

    like = Likes.query.get(str(user_id)+str(playlist_id));
    db.session.delete(like)
    playlist.hype -= 1
    db.session.commit()
    return "Unliked!"


def remove_playlist(playlist_id):
    '''deletes a playlist from the table'''

    playlist = Playlist.query.get(playlist_id)

    db.session.delete(playlist)
    db.session.commit()

    return "Playlist deleted"

## TODO: retest out different join methods make one db query, and one for loop
def show_user_plays(user_id):
    '''creates a dictionary of likes and creations
    for a given user'''

    plays = Playlist.query.filter(Playlist.creator_id==user_id).all()
    user = User.query.get(user_id)

    show = {'created': [], 'liked': []}
    for playlist in plays:
        show['created'].append({'play id': playlist.play_id, 'play name': playlist.name})
    
    for play in user.likes:
        show['liked'].append({'play id': play.play_id, 'play name': Playlist.query.get(play.play_id).name, 'author name': Playlist.query.get(play.play_id).author.name})

    return show


if __name__ == '__main__':
    from server import app
    connect_to_db(app)

