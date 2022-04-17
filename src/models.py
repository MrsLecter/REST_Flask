from enum import unique
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create instance
app = Flask(__name__)
# add db
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://**login**:**passwd**@localhost:5432/**database**'
app.config['SECRET_KEY'] = '**key**'
# initialize
db = SQLAlchemy(app)


class artists(db.Model):
    artist_id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String(50), unique=True, nullable=False)
    artist_info = db.Column(db.Text, nullable=True)

    def __init__(self, artist_name, artist_info):
        self.artist_name = artist_name
        self.artist_info = artist_info


class songs(db.Model):
    song_id = db.Column(db.Integer, primary_key=True)
    song_name = db.Column(db.String(50), unique=True, nullable=False)
    song_text = db.Column(db.Text, unique=True, nullable=False)
    song_year = db.Column(db.Integer, nullable=False)
    original_lang = db.Column(db.String(3), nullable=False)

    def __init__(self, song_id, song_name, song_text, song_year, original_lang):
        self.song_id = song_id
        self.song_name = song_name
        self.song_text = song_text
        self.song_year = song_year
        self.original_lang = original_lang


class albums(db.Model):
    album_id = db.Column(db.Integer, primary_key=True)
    album_name = db.Column(db.String(45), unique=True, nullable=False)
    album_year = db.Column(db.Integer, nullable=False)
    album_info = db.Column(db.Text, unique=True, nullable=False)

    def __init__(self, album_id, albumm_name, album_year, album_info):
        self.album_id = album_id
        self.album_name = albumm_name
        self.album_year = album_year
        self.album_info = album_info


class artist_album(db.Model):
    artist_id=db.Column(db.Integer, db.ForeignKey('artist_id'), primary_key=True)
    album_id = db.Column(db.Integer,db.ForeignKey('album_id'), primary_key=True)

    def __init__(self, artist_id, album_id):
        self.artist_id = artist_id
        self.album_id  = album_id


class album_song(db.Model):
    album_id = db.Column(db.Integer,db.ForeignKey('album_id'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song_id'),primary_key=True)

    def __init__(self, album_id, song_id):
        self.album_id = album_id
        self.song_id = song_id



db.create_all()