#!/usr/bin/python3
import typing
from typing import Dict
from venv import create
import psycopg2
from configparser import ConfigParser
import models

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# create instance
app = Flask(__name__)
# add db
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:psql@localhost:5432/db_music'
app.config['SECRET_KEY'] = 'supersecret_key'
# initialize
db = SQLAlchemy(app)


def getItems(table_name, item_name='none', item_id='none'):
    if table_name == 'artists':
        if item_name == 'none':
            requested_data = models.artists.query.all()
        else:
            requested_data = models.artists.query.filter_by(
                artist_name=item_name).first()
    elif table_name == 'albums':
        if item_name == 'none':
            requested_data = models.albums.query.all()
        else:
            requested_data = models.albums.query.filter_by(
                album_name=item_name).first()
    elif table_name == 'songs':
        if item_name == 'none':
            requested_data = models.songs.query.all()
        else:
            requested_data = models.songs.query.filter_by(
                song_name=item_name).first()
    elif table_name == 'artist_album':
        if item_name == 'artist':
            requested_data = models.artist_album.query.filter_by(
                artist_id=item_id).all()
        elif item_name == 'album':
            requested_data = models.artist_album.query.filter_by(
                album_id=item_id).all()
    elif table_name == 'album_song':
        if item_name == 'album':
            requested_data = models.album_song.query.filter_by(
                album_id=item_id).all()
        elif item_name == 'song':
            requested_data = models.album_song.query.filter_by(
                song_id=item_id).all()
    return requested_data


def postItem(table_name, item_object):
    if table_name == 'artists':
        item_model = models.artists(
            item_object['artist_name'], item_object['artist_info'])
    elif table_name == 'songs':
        item_model = models.songs(
            item_object['song_name'], item_object['song_text'], item_object['song_year'], item_object['original_lang'])
    elif table_name == 'albums':
        item_model = models.albums(
            item_object['album_name'], item_object['album_year'], item_object['album_info'])
    elif table_name == 'aritst_song':
        item_model = models.artist_album(
            item_object['artist_id'], item_object['album_id'])
    elif table_name == 'album_song':
        item_model = models.album_song(
            item_object['album_id'], item_object['song_id'])

    db.session.add(item_model)
    db.session.commit()


def searchItems(table_name, item_name):
    if table_name == 'artists':
        requested_data = models.artists.query.filter(
            models.artists.artist_name.like(f'%{item_name}%')).all()
    elif table_name == 'albums':
        requested_data = models.albums.query.filter(
            models.albums.album_name.like(f'%{item_name}%')).all()
    elif table_name == 'songs':
        requested_data = models.songs.query.filter(
            models.songs.song_name.like(f'%{item_name}%')).all()
    return requested_data


def deleteItem(table_name, item_name, item_id):
    if table_name == 'artists':
        item_model = models.artists.query.filter(
            models.artists.artist_name == item_name)
    elif table_name == 'songs':
        item_model = models.songs.query.filter(
            models.songs.song_name == item_name)
    elif table_name == 'albums':
        item_model = models.albums.query.filter(
            models.albums.album_name == item_name)
    elif table_name == 'aritst_album':
        if item_name == 'artist':
            item_model = models.artist_album.query.filter(
                models.artist_album.album_id == item_id)
        elif item_name == 'album':
            item_model = models.artist_album.query.filter(
                models.artist_album.album_id == item_id)
    elif table_name == 'album_song':
        if item_name == 'album':
            item_model = models.album_song.query.filter(
                models.album_song.album_id == item_id)
        elif item_name == 'song':
            item_model = models.album_song.query.filter(
                models.album_song.song_id == item_id)

    db.session.delete(item_model)
    db.session.commit()


def updateItem(table_name, item_object):
    if table_name == 'artists':
        requested_data = models.artists.query.filter_by(
            artist_name=item_object['artist_name']).first()

        requested_data.artist_name = item_object['artist_name']
        requested_data.artist_info = item_object['artist_info']

    elif table_name == 'albums':
        requested_data = models.albums.query.filter_by(
            album_name=item_object['album_name']).first()

        requested_data.album_name = item_object['album_name']
        requested_data.album_year = item_object['album_year']
        requested_data.album_info = item_object['album_info']

    elif table_name == 'songs':
        requested_data = models.songs.query.filter_by(
            song_name=item_object['song_name']).first()

        requested_data.song_name = item_object['song_name']
        requested_data.song_text = item_object['song_text']
        requested_data.song_year = item_object['song_year']
        requested_data.original_lang = item_object['original_lang']

    db.session.commit()


def getAlbumsForArtist(artist_name):
    requested_data = models.albums.query\
        .join(models.artists, models.artists.artist_id==models.albums.artist_id)\
        .filter(models.artists.artist_name==artist_name).all()
    return requested_data


def getCurrentAlbum(artist_name, album_name):
    requested_data = models.albums.query\
        .join(models.artists, models.albums.artist_id == models.artists.artist_id)\
        .filter(models.artists.artist_name == 'John Lennon')\
        .filter(models.albums.album_name == 'Revolver').all()
    return requested_data

