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

    feats = db.relationship('Feat', back_populates='track')


class Feat(db.Model):
    '''the association link between tracks and playlists'''

    __tablename__ = 'feats'

    feat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    track_uri = db.Column(db.String, db.ForeignKey('tracks.uri'), nullable=False)
    playl_uri = db.Column(db.String, db.ForeignKey('playlists.uri'), nullable=False)

    track = db.relationship('Track', back_populates='feats')
    playlist = db.relationship('Playlist', back_populates='feats')


class Playlist(db.Model):
    '''any playlist created with the app'''

    __tablename__ = 'playlists'

    uri = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    author = db.Column(db.String, db.ForeignKey('users.user_id'), nullable=False)
    hype = db.Column(db.Integer)

    feats = db.relationship('Feat', back_populates='playlist')
    likes = db.relationship('Likes', back_populates='playlist')
    writer = db.relationship('User', back_populates='playlists')

class Likes(db.Model):
    '''the association link between users and playlists they didn't author
    can be called and showed but don't have other value'''

    __tablename__ = 'likes'

    like_id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    play_id = db.Column(db.Integer, db.ForeignKey('playlists.uri'), nullable=False)

    user = db.relationship('User', back_populates='likes')
    playlist = db.relationship('Playlist', back_populates='likes')

class User(db.Model):
    '''a user on the app'''

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uri = db.Column(db.String, nullable=True)
    name = db.Column(db.String, nullable=False)
    email= db.Column(db.String, nullable=False, unique=True)
    pw = db.Column(db.String, nullable=False)

    likes = db.relationship('Likes', back_populates='user')
    playlists = db.relationship('Playlist', back_populates='writer')

