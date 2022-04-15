from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_to_db(app, db_name):
    '''connect to database'''

    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql:///{db_name}"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    from server import app

    connect_to_db(app, "music")

class Track(db.Model):
    '''a song on spotify'''

    __tablename__ = 'tracks'

    uri = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    artist = db.Column(db.String, nullable=False)

class SeenIn(db.Model):
    '''the accessory link between tracks and playlists'''

class Playlist(db.Model):
    '''any playlist created with the app'''

    __tablename__ = 'playlists'

    uri = db.Column(db.String, primary_key=True)
    author = db.Column(db.String, nullable=False)

class Likes(db.Model):
    '''the accessory link between users and playlists they didn't author
    can be called and showed but don't have other value'''

class User(db.Model):
    '''a user on the app'''

    __tablename__ = 'users'

    id_ = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    pw = db.Column(db.String, nullable=False)

