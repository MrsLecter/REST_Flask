#!/usr/bin/python3
import typing
import json
from typing import Dict
from venv import create

from sqlalchemy import create_engine
from src import models
from src import serializers
# import serializers
# import models
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker

# create instance
app = Flask(__name__)

# add db
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:psql@postgres:5432/db_music'
app.config['SECRET_KEY'] = 'supersecret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# initialize
db = SQLAlchemy(app)
sqlalchemy = SQLAlchemy()
sqlalchemy.init_app(app)
print('connect')
# conn_url = 'postgresql+psycopg2://postgres:psql@postgres/db_music'
# engine = create_engine(conn_url)
# scoped_session(sessionmaker(bind=engine))


def getItems(table_name, item_name='none', item_id='none'):
    print('get items')
    if table_name == 'artists':
        if item_name == 'none':
            data = models.artists.query.all()
            print('data: ',data)
            return [(json.loads(serializers.ArtistsSchema().dumps(item))) for item in data]
        else:
            requested_data = models.artists.query.filter_by(
                artist_name=item_name).first()
            return json.loads(serializers.ArtistsSchema().dumps(requested_data))
    elif table_name == 'albums':
        if item_name == 'none':
            data = models.albums.query.all()
            return [(json.loads(serializers.AlbumsSchema().dumps(item))) for item in data]
        else:
            requested_data = models.albums.query.filter_by(
                album_name=item_name).first()
            return json.loads(serializers.AlbumsSchema().dumps(requested_data))
    elif table_name == 'songs':
        if item_name == 'none':
            data = models.songs.query.all()
            return [(json.loads(serializers.SongsSchema().dumps(item))) for item in data]
        else:
            requested_data = models.songs.query.filter_by(
                song_name=item_name).first()
            return json.loads(serializers.SongsSchema().dumps(requested_data))
    elif table_name == 'artist_album':
        if item_name == 'artist':
            requested_data = models.artist_album.query.filter_by(
                artist_id=item_id).all()
            return requested_data
        elif item_name == 'album':
            requested_data = models.artist_album.query.filter_by(
                album_id=item_id).all()
            return requested_data
    elif table_name == 'album_song':
        if item_name == 'album':
            requested_data = models.album_song.query.filter_by(
                album_id=item_id).all()
            return requested_data
        elif item_name == 'song':
            requested_data = models.album_song.query.filter_by(
                song_id=item_id).all()
            return requested_data


def postItem(table_name, item_object):
    if table_name == 'artists':
        errors = serializers.ArtistsSchema().validate(item_object)
        if errors:
            print(errors)
        else:
            item_model = models.artists(
                item_object['artist_name'], item_object['artist_info'])
            db.session.add(item_model)
            db.session.commit()
    elif table_name == 'songs':
        errors = serializers.SongsSchema().validate(item_object)
        if errors:
            print(errors)
        else:
            item_model = models.songs(
                item_object['song_name'], item_object['song_text'], item_object['song_year'], item_object['original_lang'])
            db.session.add(item_model)
            db.session.commit()
    elif table_name == 'albums':
        errors = serializers.AlbumsSchema().validate(item_object)
        if errors:
            print(errors)
        else:
            item_model = models.albums(
                item_object['album_name'], item_object['album_year'], item_object['album_info'])
            db.session.add(item_model)
            db.session.commit()
    elif table_name == 'aritst_song':
        item_model = models.artist_album(
            item_object['artist_id'], item_object['album_id'])
        db.session.add(item_model)
        db.session.commit()
    elif table_name == 'album_song':
        item_model = models.album_song(
            item_object['album_id'], item_object['song_id'])
        db.session.add(item_model)
        db.session.commit()


def searchItems(table_name, item_name):
    if table_name == 'artists':
        data = models.artists.query.filter(
            models.artists.artist_name.like(f'%{item_name}%')).all()
        return [(json.loads(serializers.ArtistsSchema().dumps(item))) for item in data]
    elif table_name == 'albums':
        data = models.albums.query.filter(
            models.albums.album_name.like(f'%{item_name}%')).all()
        return [(json.loads(serializers.AlbumsSchema().dumps(item))) for item in data]
    elif table_name == 'songs':
        data = models.songs.query.filter(
            models.songs.song_name.like(f'%{item_name}%')).all()
        return [(json.loads(serializers.SongsSchema().dumps(item))) for item in data]


def deleteItem(table_name, item_name):
    if table_name == 'artists':
        item = models.artists.query.filter(
            models.artists.artist_name == item_name).first()
    elif table_name == 'songs':
        item = models.songs.query.filter(
            models.songs.song_name == item_name).first()
    elif table_name == 'albums':
        item = models.albums.query.filter(
            models.albums.album_name == item_name).first()
    
    db.session.delete(item)
    db.session.commit()


def updateItem(table_name, item_object):
    if table_name == 'artists':
        errors = serializers.ArtistsSchema().validate(item_object)
        if errors:
            print(errors)
        else:
            requested_data = models.artists.query.filter_by(
                artist_name=item_object['artist_name']).first()
            requested_data.artist_name = item_object['artist_name']
            requested_data.artist_info = item_object['artist_info']

    elif table_name == 'albums':
        errors = serializers.AlbumsSchema().validate(item_object)
        if errors:
            print(errors)
        else:
            requested_data = models.albums.query.filter_by(
                album_name=item_object['album_name']).first()

            requested_data.album_name = item_object['album_name']
            requested_data.album_year = item_object['album_year']
            requested_data.album_info = item_object['album_info']

    elif table_name == 'songs':
        errors = serializers.SongsSchema().validate(item_object)
        if errors:
            print(errors)
        else:
            requested_data = models.songs.query.filter_by(
                song_name=item_object['song_name']).first()

            requested_data.song_name = item_object['song_name']
            requested_data.song_text = item_object['song_text']
            requested_data.song_year = item_object['song_year']
            requested_data.original_lang = item_object['original_lang']

    db.session.commit()


def getAlbumsForArtist(artist_name, album_name='none', song_name='none'):
    # you know only artist_name
    if album_name == 'none' and song_name == 'none':
        requested_data = models.albums.query\
            .join(models.artist_album, models.artist_album.album_id == models.albums.album_id)\
            .join(models.artists, models.artists.artist_id == models.artist_album.artist_id)\
            .filter(models.artists.artist_name == artist_name).all()
        return [(json.loads(serializers.AlbumsSchema().dumps(item))) for item in requested_data]
    # you know artist_name and album_name
    elif album_name != 'none' and song_name == 'none':
        requested_data = models.albums.query\
            .join(models.artist_album, models.artist_album.album_id == models.albums.album_id)\
            .join(models.artists, models.artists.artist_id == models.artist_album.artist_id)\
            .filter(models.artists.artist_name == artist_name)\
            .filter(models.albums.album_name == album_name).first()
        return (json.loads(serializers.AlbumsSchema().dumps(requested_data)))
    # you know artist_name and song_name
    elif album_name == 'none' and song_name != 'none':
        requested_data = models.albums.query\
            .join(models.artist_album, models.artist_album.album_id == models.albums.album_id)\
            .join(models.album_song, models.album_song.album_id == models.albums.album_id)\
            .join(models.songs, models.songs.song_id == models.album_song.song_id)\
            .join(models.artists, models.artists.artist_id == models.artist_album.artist_id)\
            .filter(models.artists.artist_name == artist_name)\
            .filter(models.songs.song_name == song_name).first()
        print(requested_data)
        return json.loads(serializers.AlbumsSchema().dumps(requested_data))
    

def getSongsForArtist(artist_name, album_name='none', song_name='none'):
    # you know only artist_name
    if album_name == 'none' and song_name == 'none':
        requested_data = models.songs.query\
            .join(models.album_song, models.album_song.song_id == models.songs.song_id)\
            .join(models.artist_album, models.artist_album.album_id == models.album_song.album_id)\
            .join(models.artists, models.artists.artist_id == models.artist_album.album_id)\
            .filter(models.artists.artist_name == artist_name).all()
    # you know artist_name and album_name
    elif album_name != 'none' and song_name == 'none':
        requested_data = models.songs.query\
            .join(models.album_song, models.album_song.song_id == models.songs.song_id)\
            .join(models.artist_album, models.artist_album.album_id == models.album_song.album_id)\
            .join(models.artists, models.artists.artist_id == models.artist_album.album_id)\
            .filter(models.artists.artist_name == artist_name)\
            .filter(models.albums.album_name == album_name).all()
    # you know artist_name, album_name and song_name
    elif album_name != 'none' and song_name != 'none':
        requested_data = models.songs.query\
            .join(models.album_song, models.album_song.song_id == models.songs.song_id)\
            .join(models.artist_album, models.artist_album.album_id == models.album_song.album_id)\
            .join(models.artists, models.artists.artist_id == models.artist_album.album_id)\
            .filter(models.artists.artist_name == artist_name)\
            .filter(models.albums.album_name == album_name)\
            .filter(models.songs.song_name == song_name).first()
        return json.loads(serializers.SongsSchema().dumps(requested_data))
    return [(json.loads(serializers.SongsSchema().dumps(item))) for item in requested_data]


def getItemId(table_name, item_name):
    if table_name == 'artists':
        requested_data = models.artists.query.filter_by(
            artist_name=item_name).first().artist_id
        return requested_data
    elif table_name == 'albums':
        requested_data = models.albums.query.filter_by(
            album_name=item_name).first().album_id
        return requested_data
    elif table_name == 'songs':
        requested_data = models.songs.query.filter_by(
            song_name=item_name).first().song_id
        return requested_data


def deleteSong(album_name, song_name):
    current_song_id = getItemId('songs', song_name)
    current_album_id = getItemId('albums', album_name)
    song_string = models.songs.query.filter(
            models.songs.song_name ==song_name).first()
    album_song_string = models.album_song.query.filter(
            models.album_song.song_id == current_song_id )\
            .filter(models.album_song.album_id == current_album_id).first()
    db.session.delete(song_string)
    db.session.delete(album_song_string)
    db.session.commit()
   

def deleteAlbum(artist_name, album_name):
    current_album_id = getItemId('albums', album_name)
    current_artist_id = getItemId('artist', artist_name)
    album_string = models.albums.query.filter(
            models.albums.album_name == album_name).first()
    artist_album_string = models.artist_album.query.filter(
            models.artist_album.album_id == current_album_id)\
            .filter(models.artist_album.artist_id == current_artist_id).first()
    album_song_strings = models.album_song.query.filter(
            models.album_song.album_id == current_album_id).all()
    db.session.delete(album_string)
    db.session.delete(artist_album_string)
    for item in album_song_strings:
        db.session.delete(item)
    db.session.commit()


def deleteArtist(artist_name):
    current_artist_id = getItemId('artists', artist_name)
    artist_string = models.artists.query.filter(
            models.artists.artist_name == artist_name).first()
    artist_album_string = models.artist_album.query.filter(
            models.artist_album.artist_id == current_artist_id).first()
    db.session.delete(artist_string)
    db.session.delete(artist_album_string)
    db.session.commit()


def clearItemsWithoutReferences():
    songs = models.songs.query.all()
    album_song = models.album_song.query.all()
    albums = models.albums.query.all()
    artist_album = models.artist_album.query.all()
    artist = models.artists.query.all()

    song_ids = []
    album_song_ids = []
    album_ids = []
    artist_album_alids = []
    artist_album_arids = []
    artist_ids = []

    for i_song, i_album_song, i_album, i_artist_album, i_artist in zip(songs,album_song,albums, artist_album, artist) :
        song_ids.append(i_song.song_id)
        album_song_ids.append(i_album_song.song_id)

        album_ids.append(i_album.album_id)
        artist_album_alids.append(i_artist_album.album_id)

        artist_album_arids.append(i_artist_album.artist_id)
        artist_ids.append(i_artist.artist_id)

    songNoLink = list(set(song_ids) - set(album_song_ids))
    album_songNoLink = list(set(album_song_ids) - set(song_ids))

    albumNoLink = list(set(album_ids) - set(artist_album_alids))
    artist_albumsNoLink = list(set(artist_album_alids) - set(album_ids))

    artistNoLink = list(set(artist_ids) - set(artist_album_arids))
    artists_albumNoLink = list(set(artist_album_arids) - set(artist_ids))

    if len(songNoLink) != 0:
        for item in songNoLink:
            obj = models.songs.query.filter_by(song_id=item).first()
            db.session.delete(obj)
        db.session.commit()
    if len(albumNoLink) != 0:
        for item in albumNoLink:
            obj = models.albums.query.filter_by(album_id=item).first()
            db.session.delete(obj)
        db.session.commit()
    if len(artistNoLink) != 0:
        for item in artistNoLink:
            obj = models.artists.query.filter_by(artist_id=item).first()
            db.session.delete(obj)
        db.session.commit()
    if len(album_songNoLink) != 0:
        for item in album_songNoLink:
            obj = models.album_song.query.filter_by(song_id=item).first()
            db.session.delete(obj)
        db.session.commit()
    if len(artist_albumsNoLink) != 0:
        for item in artist_albumsNoLink:
            obj = models.artist_album.query.filter_by(album_id=item).first()
            db.session.delete(obj)
        db.session.commit()
    if len(artists_albumNoLink) != 0:
        for item in artists_albumNoLink:
            obj = models.artist_album.query.filter_by(artist_id=item).first()
            db.session.delete(obj)
        db.session.commit()

