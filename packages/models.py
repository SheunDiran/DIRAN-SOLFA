from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    users_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    users_firstname = db.Column(db.String(100), nullable=False)
    users_lastname = db.Column(db.String(100), nullable=False)
    users_email = db.Column(db.String(150), nullable=False, unique=True)
    users_phonenumber = db.Column(db.String(100), nullable=False, unique=True)
    users_password = db.Column(db.String(200), nullable=False)
    users_profilepicture = db.Column(db.BLOB)
    user_verified = db.Column(db.BLOB)
    users_role = db.Column(db.String(150), nullable=False)
    date_registered = db.Column(db.DateTime, default=datetime.utcnow)
    date_loggedin = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_instru= db.Column(db.Integer, db.ForeignKey('instruments.instru_id'))
    def __repr__(self):
        return f"{self.users_firstname} {self.users_lastname}"

class Instruments(db.Model):
    instru_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f"{self.name}"

class User_Instrument(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.users_id'))
    instrument_id = db.Column(db.Integer, db.ForeignKey('instruments.instru_id'))
    
    user = db.relationship("User", backref="instruments")
    instrument = db.relationship("Instruments", backref="users")
    def __repr__(self):
        return f"{self.user_id}  {self.instrument_id}"

class Artists(db.Model):
    artist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    artist_firstname = db.Column(db.String(100), nullable=False)
    artist_lastname = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f"{self.artist_firstname} {self.artist_lastname}"
    
class Songs(db.Model):
    songs_id = db.Column(db.Integer, primary_key=True)
    songs_title = db.Column(db.String(100), nullable=False)
    song_lyrics = db.Column(db.Text, nullable=False)
    approved = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"{self.songs_title}"
    
class ArtistSongs(db.Model):
    __tablename__ = 'artist_songs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.artist_id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.songs_id'), nullable=False)
    tonic_solfa = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    artist = db.relationship("Artists", backref="artist_songs", foreign_keys=[artist_id])
    song = db.relationship("Songs", backref="artist_songs", foreign_keys=[song_id])

    def __repr__(self):
        return f"{self.id}"





class Song_solfa(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.songs_id'))
    instrument_id = db.Column(db.Integer, db.ForeignKey('instruments.instru_id'))
    solfa_notation = db.Column(db.Text)

    song = db.relationship("Songs", backref="song_solfa", foreign_keys=[song_id])
    def __repr__(self):
        return f"{self.id}"

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"{self.id}"