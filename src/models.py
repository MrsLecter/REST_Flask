from enum import unique
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint


# create instance
app = Flask(__name__)
# add db
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:psql@localhost:5432/db_music'
app.config['SECRET_KEY'] = 'supersecret_key'
# initialize
db = SQLAlchemy(app)


class artists(db.Model):
    __tablename__='artists'
    artist_id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String(50), unique=True, nullable=False)
    artist_info = db.Column(db.Text, nullable=False)
    albums = db.relationship("albums", secondary='artist_album')

    def __init__(self, artist_name, artist_info):
        self.artist_name = artist_name
        self.artist_info = artist_info


class albums(db.Model):
    __tablename__='albums'
    album_id = db.Column(db.Integer, primary_key=True)
    album_name = db.Column(db.String(45), unique=True, nullable=False)
    album_year = db.Column(db.Integer, nullable=False)
    album_info = db.Column(db.Text, unique=True, nullable=False)
    artists = db.relationship("artists", secondary='artist_album')
    songs = db.relationship("songs", secondary='album_song')
    
    def __init__(self, album_id, albumm_name, album_year, album_info):
        self.album_id = album_id
        self.album_name = albumm_name
        self.album_year = album_year
        self.album_info = album_info

class songs(db.Model):
    __tablename__='songs'
    song_id = db.Column(db.Integer, primary_key=True)
    song_name = db.Column(db.String(50), unique=True, nullable=False)
    song_text = db.Column(db.Text, unique=True, nullable=False)
    song_year = db.Column(db.Integer, nullable=False)
    original_lang = db.Column(db.String(3), nullable=False)
    albums = db.relationship("albums", secondary='album_song')

    def __init__(self, song_id, song_name, song_text, song_year, original_lang):
        self.song_id = song_id
        self.song_name = song_name
        self.song_text = song_text
        self.song_year = song_year
        self.original_lang = original_lang

class artist_album(db.Model):
    __tablename__='artist_album'
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.artist_id'))
    album_id = db.Column(db.Integer, db.ForeignKey('albums.album_id'))
    __table_args__ = (PrimaryKeyConstraint (artist_id, album_id),{},)
    
    def __init__(self, artist_id, album_id):
        self.artist_id = artist_id
        self.album_id = album_id

class album_song(db.Model):
    __tablename__='album_song'
    album_id = db.Column(db.Integer,  db.ForeignKey('albums.album_id'))
    song_id = db.Column(db.Integer,  db.ForeignKey('songs.song_id'))
    __table_args__ = (PrimaryKeyConstraint (album_id, song_id),{},)

    def __init__(self, album_id, song_id):
        self.album_id = album_id
        self.song_id = song_id


db.create_all()

