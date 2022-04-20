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
            track, tracks[track][0], tracks[track][1])
        track_list.append(new)

    model.db.session.add_all(track_list)
    model.db.session.commit()

    return tracks

fill_tracks()


def fill_users():
    new = [crud.create_user('Admin', 'hbplaymaker@gmail.com', os.environ['APP_PASS'], os.environ['APP_ID'])]

    for n in range(2, 20):
        email = f'test{n}@email.com'
        name = str(n)+'@gmail.com'
        pw = f'{n}{n+1}{n+2}{n+3}'

        new.append(crud.create_user(email, pw, name))

    new.append(crud.create_user('The Boss', 'kayejrosen@gmail.com', os.environ['ME_PASS'], os.environ['ME_ID']))

    model.db.session.add_all(new)
    model.db.session.commit()

# fill_users()

