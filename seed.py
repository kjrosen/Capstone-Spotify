"""Script to seed the database"""

## import needed python files, and os for commands
import os

import crud
import model
import server

## give the commands to drop and recreate db
os.system('dropdb music')
os.system('createdb music')

model.connect_to_db(server.app)
model.db.create_all()

## TODO: perform number of API searches to load tracks into db
## save the db in a sql file
## reload that sql file here to seed it as a reset

model.db.session.add_all()
model.db.session.commit()