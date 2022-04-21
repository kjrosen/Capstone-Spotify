'''the model for each tabel in app database - called "music" '''

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_to_db(app, db_name="music"):
    '''connect to database'''

    ## basic install requirements from sqlalchemy docs
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql:///{db_name}"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    ## initializes connection between the Flask app and the database
    db.app = app
    db.init_app(app)
    print("Connected to the db!")


class Track(db.Model):
    '''a song on spotify (PK is the URI used to locate on Spotify) 
    connected to playlists by Feats'''

    __tablename__ = 'tracks'

    track_id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    artist = db.Column(db.String, nullable=False)

    feats = db.relationship('Feat', back_populates='track')

    def __repr__(self):
        return f'<Track title={self.title} artist={self.artist}>'


class Feat(db.Model):
    '''the association link between tracks and playlists
    tracks can be featured on many playlists, or on the same playlist many times
    a playlist can feature many songs, sometimes more than once'''

    __tablename__ = 'feats'

    feat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    track_id = db.Column(db.String, db.ForeignKey('tracks.track_id'), nullable=False)
    play_id = db.Column(db.String, db.ForeignKey('playlists.play_id'), nullable=False)

    track = db.relationship('Track', back_populates='feats')
    playlist = db.relationship('Playlist', back_populates='feats')

    def __repr__(self):
        return f'<Feat connecting Track={self.track.title} to Playlist={self.playlist.name}>'


class Playlist(db.Model):
    '''any playlist created with the app
    PK is Spotify URI (for embedding), name is the phrase that makes up the track titles
    
    creator_id is the user that created the playlist, findable by self.author
    connected to tracks with feats: 
        songlist can be found by utilizing feats (playlist.feats)
    likeable by many users
    '''

    __tablename__ = 'playlists'

    play_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    hype = db.Column(db.Integer)

    feats = db.relationship('Feat', back_populates='playlist')
    likes = db.relationship('Likes', back_populates='playlist')
    author = db.relationship('User', back_populates='playlists')

    def __repr__(self):
        return f'<Playlist name={self.name} author={self.author.name}>'


class Likes(db.Model):
    '''the association link between users and playlists they didn't author
    a user can only like a playlist once, PK is string combo of user+playlist PKs
    '''

    __tablename__ = 'likes'

    like_id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    play_id = db.Column(db.String, db.ForeignKey('playlists.play_id'), nullable=False)

    user = db.relationship('User', back_populates='likes')
    playlist = db.relationship('Playlist', back_populates='likes')

    def __repr__(self):
        return f'<Like connecting User={self.user.name} to Playlist={self.playlist.name}>'


class User(db.Model):
    '''a user on the app
    PK is app-specific id, URI to find Spotify account optional

    all playlists liked findable with user.likes
    all playlists authored findable with user.playlists
    '''

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    spot_id = db.Column(db.String, nullable=True)
    name = db.Column(db.String, nullable=False)
    email= db.Column(db.String, nullable=False, unique=True)
    pw = db.Column(db.String, nullable=False)

    likes = db.relationship('Likes', back_populates='user')
    playlists = db.relationship('Playlist', back_populates='author')

    def __repr__(self):
        return f'<User name={self.name} user_id={self.user_id}>'


if __name__ == "__main__":
    from server import app

    ## imports the Flask app from the server and connects to the db
    connect_to_db(app)