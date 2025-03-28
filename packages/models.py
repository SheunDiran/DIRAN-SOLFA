from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Instruments(db.Model):
    instru_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    instr_name=db.Column(db.String(100),nullable=False)
    instru_type=db.Column(db.String(100),nullable=False)

    def __repr__(self):
        return {self.instr_name}
    
class User_Instrument(db.Model):
    user_instru_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.users_id'))  
    instrument_id=db.Column(db.Integer,db.ForeignKey('instruments.instru_id'))  

    def __repr__(self):
        return {self.user_instru_id}
    
class Artists(db.Model):
    artist_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    artist_firstname=db.Column(db.String(100),nullable=False)
    artist_lastname=db.Column(db.String(100),nullable=False) 

    def __repr__(self):
        return {self.artist_firstname}
    
class Song_solfa(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    song_id=db.Column(db.Integer,db.ForeignKey('songs.songs_id')) 
    instrument_id=db.Column(db.Integer,db.ForeignKey('instruments.instru_id'))  
    solfa_notation=db.Column(db.Text)

    def __repr__(self):
        return {self.id}
    
class Songs_artist(db.Model):
      song_artist_id=db.Column(db.Integer,primary_key=True,autoincrement=True) 
      song_id=db.Column(db.Integer,db.ForeignKey('songs.songs_id')) 
      artist_id=db.Column(db.Integer,db.ForeignKey('artists.artist_id'))  
    
      def __repr__(self):
        return {self.song_artist_id}

class Requests(db.Model):
     requests_id=db.Column(db.Integer,primary_key=True,autoincrement=True) 
     user_id=db.Column(db.Integer,db.ForeignKey('user.users_id'))
     song_id=db.Column(db.Integer,db.ForeignKey('songs.songs_id'))
     request_message=db.Column(db.TEXT,nullable=False)
     date_requested=db.Column(db.DateTime(),default=datetime.utcnow) 

     def __repr__(self):
                 return {self.requests_id}

class Songs(db.Model):
     songs_id=db.Column(db.Integer,primary_key=True,autoincrement=True)     
     songs_title=db.Column(db.String(200),nullable=False)
     song_lyrics=db.Column(db.TEXT,nullable=False)
     date_added=date_requested=db.Column(db.DateTime(),default=datetime.utcnow) 

     def __repr__(self):
                 return {self.songs_title}
class User(db.Model):
     users_id=db.Column(db.Integer,primary_key=True,autoincrement=True) 
     users_firstname=db.Column(db.String(100),nullable=False)    
     users_lastname=db.Column(db.String(100),nullable=False)  
     users_email=db.Column(db.String(150),nullable=False,unique=True)  
     users_phonenumber=db.Column(db.String(100),nullable=False,unique=True) 
     users_password=db.Column(db.String(45),nullable=False,unique=True)  
     users_profilepicture=db.Column(db.BLOB,nullable=False)
     user_verified=db.Column(db.BLOB,nullable=False)
     users_role=db.Column(db.Enum('user', 'scorers'))
     date_registered=date_requested=db.Column(db.DateTime(),default=datetime.utcnow)  
     date_loggedin=db.Column(db.DateTime(),default=datetime.utcnow,onupdate=datetime.utcnow) 
     
     def __repr__(self):
                 return {self.users_firstname}
class Admin(db.Model):
      admin_id=db.Column(db.Integer,primary_key=True,autoincrement=True) 
      username=db.Column(db.String(100),nullable=False)
      email=db.Column(db.String(100),nullable=False,unique=True)
      password=db.Column(db.String(100),nullable=False,unique=True)
      last_loggedin=db.Column(db.DateTime(),default=datetime.utcnow,onupdate=datetime.utcnow) 




    