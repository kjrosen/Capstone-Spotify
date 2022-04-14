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

class Track(db.model):
    '''a song on spotify'''

    __tablename__ = 'tracks'

    track_uri = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)

