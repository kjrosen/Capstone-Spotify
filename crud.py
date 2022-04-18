"""logic/functions/methods for database"""

from model import Track, Feat, Playlist, Likes, User, connect_to_db, db

def check_email(email):
    '''checks if email is already in db'''

    print()
    print(email)
    check = User.query.filter(User.email==email).all()
    print(check)
    print()

    return (len(check) == 1, check)
    

def log_in(email, password):
    '''checks a user's password, returns true if logged in
    flase if password wrong'''

    user = check_email(email)

    if user[0] == True:

        if user[1][0].pw == password:
            return True
        else:
            return False


def create_account(email, password, name):
    user = check_email(email)

    if user[0] == False:
        new = create_user(name=name, email=email, pw=password)
        db.session.add(new)
        db.session.commit()
        return True
    else: 
        return False


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


def create_playlist(URI, name, creator):
    """Create and return a new playlist"""

    playlist = Playlist(
        uri=URI, 
        name=name, 
        creator_id=creator)

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


if __name__ == '__main__':
    from server import app
    connect_to_db(app)