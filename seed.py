"""Script to seed the database"""

## import needed python files, and os for commands
import os

import crud
import model
import server
import json

## give the commands to drop and recreate db
os.system('dropdb music')
os.system('createdb music')

model.connect_to_db(server.app)
model.db.create_all()

## songs collected from letters and common word searches
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



file = open('data/playlists.json').read()
all_plays = json.loads(file)

def fill_playlists(plays=all_plays):
    
    play_list = []
    for play in plays:
        new = crud.create_playlist(
            play, 
            plays[play][0], 
            plays[play][1],
            plays[play][2],
        )

        play_list.append(new)


    model.db.session.add_all(play_list)
    model.db.session.commit()

fill_playlists()
