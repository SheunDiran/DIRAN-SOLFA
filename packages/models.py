from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Instruments(db.Model):
    instru_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f"{self.name}"

class User__Instrument(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.users_id'))
    instrument_id = db.Column(db.Integer, db.ForeignKey('instruments.instru_id'))
    
    user = db.relationship("User", backref="instruments")
    instrument = db.relationship("Instruments", backref="users")
    def __repr__(self):
        return f"{self.user_id}  {self.instrument_id}"


    
class Songs(db.Model):
    songs_id = db.Column(db.Integer, primary_key=True)
    songs_title = db.Column(db.String(100), nullable=False)
    song_lyrics = db.Column(db.Text, nullable=False)
    approved = db.Column(db.Boolean, default=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=True)
    admin = db.relationship('Admin', backref=db.backref('songs', lazy=True))

    def __repr__(self):
        return f"{self.songs_title}"
    



class SongsRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_title = db.Column(db.String(100), nullable=False)
    song_lyrics = db.Column(db.Text, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.artist_id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.users_id'), nullable=True)
    solfa_notation = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(100), nullable=False, default='pending')
    artist = db.relationship('Artists', backref='songs_requests', lazy=True)
    user = db.relationship('User', backref='songs_requests', lazy=True, foreign_keys=[user_id])


class User(db.Model):
    users_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    users_firstname = db.Column(db.String(100), nullable=False)
    users_lastname = db.Column(db.String(100), nullable=False)
    users_email = db.Column(db.String(150), nullable=False, unique=True)
    users_phonenumber = db.Column(db.String(100), nullable=True, unique=True)
    users_password = db.Column(db.String(200), nullable=False)
    users_profilepicture = db.Column(db.String(128), nullable=True)
    user_verified = db.Column(db.BLOB)
    users_role = db.Column(db.String(150), nullable=False)
    date_registered = db.Column(db.DateTime, default=datetime.utcnow)
    date_loggedin = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_instru = db.Column(db.Integer, db.ForeignKey('instruments.instru_id'))

    def __repr__(self):
        return f"{self.users_firstname} {self.users_lastname}"

class Artists(db.Model):
    artist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    artist_firstname = db.Column(db.String(100), nullable=False)
    artist_lastname = db.Column(db.String(100), nullable=False)
    artist_dp = db.Column(db.String(128), nullable=True)

    def __repr__(self):
        return f"{self.artist_firstname} {self.artist_lastname}"
    
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
    dp = db.Column(db.String(100),nullable=True)
    def __repr__(self):
        return f"{self.id}"
    
class SearchHistory(db.Model):
    __tablename__='search_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.users_id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.artist_id'))
    search_term = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    song_id = db.Column(db.Integer, db.ForeignKey('songs.songs_id'))  # Update this line
    song = db.relationship('Songs', backref=db.backref('search_history', lazy=True), foreign_keys=[song_id])