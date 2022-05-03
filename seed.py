"""Script to seed the database"""

## import needed python files, and os for commands
import os

import crud
import model
from server import app
import json

## give the commands to drop and recreate db
os.system('dropdb music')
os.system('createdb music')
# os.system('source secrets.sh')
# os.system('psql music < data/musicBack.sql')

model.connect_to_db(app)
model.db.create_all()



# takes users from users.json and fills into database
file = open('data/users.json').read()
all_users = json.loads(file)

def fill_users(users=all_users):

    user_list = []
    for user_ in users:
        new = crud.create_user(
            users[user_][1], 
            users[user_][2], 
            users[user_][3],
            users[user_][0],
        )

        user_list.append(new)


    model.db.session.add_all(user_list)
    model.db.session.commit()

fill_users()


## cached songs collected from letters and common word searches
file = open('data/tracks.json').read()
all_tracks = json.loads(file)
def fill_tracks(tracks=all_tracks):
    '''take in a json file and seed the tracks table of db'''

    track_list = []
    for track in tracks:
        
        new = crud.create_track(
            track, 
            tracks[track][0], 
            tracks[track][1]
            )
        track_list.append(new)

    model.db.session.add_all(track_list)
    model.db.session.commit()

    return tracks

fill_tracks()


## makes an api search to get all tracks from a playlist, save if not in db, and create feat
def make_feats(play_id):

    tracks = crud.spot.playlist_items(play_id)
    items = tracks['items']
    feats = []
    for item in items:
        id = item['track']['id']
        title = item['track']['name']
        artist = item['track']['artists'][0]['name']


        if crud.Track.query.get(id) == None:
            song = crud.create_track(id, title, artist)
            crud.db.session.add(song)
            crud.db.session.commit()

        feat = crud.create_feat(id, play_id)
        feats.append(feat)

    crud.db.session.add_all(feats)
    crud.db.session.commit()

    return feats


## takes playlists from admin spotify account and creates tracks and feats for them
all_plays = crud.spot2.user_playlists(crud.app_id)
def fill_playlists_and_feats(playlists=all_plays):
    '''fills the music db with each playlist, iterates through the results to make playlists out of them'''

    items = playlists['items']
    plays = []
    for play in items:
        id_ = play['id']
        name = play['name']
        playlist = crud.create_playlist(id_, name, 1)
        plays.append(playlist)

        # make_feats(id_)

    crud.db.session.add_all(plays)
    crud.db.session.commit()

fill_playlists_and_feats()

all_plays = model.Playlist.query.all()
for play in all_plays:
    make_feats(play.play_id)

# file = open('data/plays.json').read()
# all_plays = json.loads(file)

# def fill_playlists(plays=all_plays):
    
#     play_list = []
#     for play in plays:
#         new = crud.create_playlist(
#             play, 
#             plays[play][0], 
#             plays[play][1],
#             plays[play][2],
#         )

#         play_list.append(new)


#     model.db.session.add_all(play_list)
#     model.db.session.commit()

# fill_playlists()