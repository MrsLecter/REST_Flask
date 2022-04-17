from flask import Flask, request, render_template, redirect, jsonify, abort

from src import db_managing
from src import JSONconverter
from src import translator
from src import utils

from logging import FileHandler, WARNING, INFO
from http import HTTPStatus

import json
import logging
import time

app = Flask(__name__)

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
#add logging
if not app.debug:
    file_handler = FileHandler('errorlog.txt')
    file_handler.setLevel(WARNING)
    app.logger.addHandler(file_handler)

#TODO: Запросы на несуществующие ресурсы (например, /some/non/existing/resource) корректно обрабатываются (возвращается human friendly сообщение и 404 статус код)


@app.route('/', methods=['GET'])
def home_page():
    if request.method == 'GET':
        #show home page
        return render_template("index.html", title='home page', data={'hello world'}), HTTPStatus.OK.value

#TODO:Сервер возвращает статус код 400 и соответствующее сообщение, если тело запроса не содержит обязательных полей
@app.route('/artists', methods=['GET', 'POST'])
def all_artists():
    if request.method == 'GET':
        artists_data = JSONconverter.getJSONFromList(
            db_managing.getItems('artists'))
        return render_template("index.html", title='artists page', data=artists_data), HTTPStatus.OK.value
    elif request.method == 'POST':
        #load data from request
        request_data = json.loads(request.get_data().decode('UTF-8'))
        #items existence test
        ifItemExist = bool(db_managing.getItemId("artists", request_data["artist_name"]))
        #if not exist
        if ifItemExist == False:
            #put item into data base
            db_managing.postItem('artists', request_data)
            return render_template("index.html", title='artists page', data=['Item added successfully']), HTTPStatus.CREATED.value
        #if item already exists
        elif ifItemExist == True:
            return render_template("index.html", title='artists page', data=['Item already exists!']), HTTPStatus.CONFLICT.value

#TODO: delete linked songs and albums 
@app.route('/artists/<artist_name>', methods=['GET', 'PUT', 'DELETE'])
def current_artist(artist_name):
    if request.method == 'GET':
        current_artist_data = JSONconverter.getJSONFromList(
            db_managing.getItems('artists', artist_name))
        return render_template("index.html", title='current artists page', data=current_artist_data), 200
    elif request.method == 'PUT':
        #ask for request data
        request_data = json.loads(request.get_data().decode('UTF-8'))
        #ask for item id in an existing database
        item_id = db_managing.getItemId('artists' , request_data['artist_name'])
        #items existence test
        ifItemExist = bool(item_id)
        #if items already exist
        if ifItemExist == True:
            #add to current data id
            request_data['artist_id'] = item_id
            #put into data base with new data
            db_managing.updateItem('artists', request_data)
            #Informing the user about changes
            return render_template("index.html", title='artists page', data=['Item updated successfully']), HTTPStatus.OK.value
        #if item doesn't exist
        elif ifItemExist == False:
            #Informing the user about changes
            return render_template("index.html", title='current artists page', data=['Item not found!']), HTTPStatus.NOT_FOUND.value
    elif request.method == 'DELETE':
        request_data = json.loads(request.get_data().decode('UTF-8'))
        item_id = db_managing.getItemId('artists' , request_data['artist_name'])
        ifItemExist = bool(item_id)
        if ifItemExist == True:
            #ask data base all album_id which links with current artist_id
            all_albums_id = utils.getRequiredId(db_managing.getItems('artist_albums', 'artist', item_id), 1)
            #delete artist item from the table artists
            db_managing.deleteItem('artists', item_id)
            #delete row artist_id--album_id from linking table artist_album
            db_managing.deleteItem('artist_album', item_id, 'album')
            #TODO: delete items without links
            return render_template("index.html", title='current artists page', data=['Item deleted successfully!']), HTTPStatus.ACCEPTED.value
        elif ifItemExist == False:
            return render_template("index.html", title='current artists page', data=['Item not found!']), HTTPStatus.NOT_FOUND.value


@app.route('/artists/<artist_name>/albums', methods=['GET', 'POST'])
def all_albums(artist_name):
    if request.method == 'GET':
        all_albums_data = JSONconverter.getJSONFromList(
            db_managing.getAlbumsForArtist(artist_name))
        return render_template("index.html", title='all albums page', data=all_albums_data), HTTPStatus.OK.value
    elif request.method == 'POST':
        #load data from request
        request_data = json.loads(request.get_data().decode('UTF-8'))
        #items existence test
        ifItemExist = bool(db_managing.getItemId("albums", request_data["album_name"]))
        #if not exist
        if ifItemExist == False:
            #put item into data base
            db_managing.postItem('albums', request_data)
            #ask db for artist_id
            artist_id = db_managing.getItemId('artists' , artist_name)
            #ask db for new album_id
            album_id = db_managing.getItemId('albums' , request_data['album_name'])
            #post artist_id and album_id to linking table artist_album
            db_managing.postItem('artist_album',{"artist_id": artist_id, "album_id": album_id})
            return render_template("index.html", title='albums page', data=['Item added successfully']), HTTPStatus.CREATED.value
        #if item exists
        elif ifItemExist == True:
            return render_template("index.html", title='albums page', data=['Item already exists!']), HTTPStatus.CONFLICT.value


@app.route('/artists/<artist_name>/albums/<album_name>', methods=['GET', 'PUT', 'DELETE'])
def current_album(artist_name, album_name):
    if request.method == 'GET':
        current_album_data = JSONconverter.getJSONFromList(
            db_managing.getCurrentAlbum(artist_name, album_name))
        return render_template("index.html", title='current album page', data=current_album_data), HTTPStatus.OK.value
    elif request.method == 'PUT':
        #ask for request data
        request_data = json.loads(request.get_data().decode('UTF-8'))
        #ask for item id in an existing database
        item_id = db_managing.getItemId('albums' , request_data['album_name'])
        #items existence test
        ifItemExist = bool(item_id)
        #if items already exist
        if ifItemExist == True:
            #add to current data id
            request_data['album_id'] = item_id
            #put into data base with new data
            db_managing.updateItem('albums', request_data)
            #Informing the user about changes
            return render_template("index.html", title='current album page', data=['Item updated successfully']), HTTPStatus.OK.value 
        #if item doesn't exist
        elif ifItemExist == False:
            #Informing the user about changes
            return render_template("index.html", title='current album page', data=['Item not found!']), HTTPStatus.NOT_FOUND.value
    elif request.method == 'DELETE':
        request_data = json.loads(request.get_data().decode('UTF-8'))
        item_id = db_managing.getItemId('albums' , request_data['album_name'])
        ifItemExist = bool(item_id)
        if ifItemExist == True:
            db_managing.deleteItem('albums', item_id)
            #delete album from linking table artist_album
            db_managing.deleteItem('artist_album', item_id, 'album')
            return render_template("index.html", title='current album page', data=['Item deleted successfully!']), HTTPStatus.ACCEPTED.value
        elif ifItemExist == False:
            return render_template("index.html", title='current album page', data=['Item not found!']), HTTPStatus.NOT_FOUND.value


@app.route('/artists/<artist_name>/songs', methods=['GET'])
def show_all_songs(artist_name):
    if request.method == 'GET':
        all_songs_data = JSONconverter.getJSONFromList(
            db_managing.getSongsForArtist(artist_name))
        return render_template("index.html", title='all songs page', data=all_songs_data), 200


@app.route('/artists/<artist_name>/songs/<song_name>', methods=['GET'])
def current_song(artist_name, song_name):
    if request.method == 'GET':
        album_name = db_managing.getAlbumForSong(artist_name, song_name)
        return redirect(f"http://localhost:5000/artists/{artist_name}/albums/{album_name}/songs/{song_name}", code=301)


@app.route('/artists/<artist_name>/albums/<album_name>/songs', methods=['GET', 'POST'])
def songs_current_album(artist_name, album_name):
    if request.method == 'GET':
        current_album_data = JSONconverter.getJSONFromList(
            db_managing.getSongsForAlbums(artist_name, album_name))
        return render_template("index.html", title='current album page', data=current_album_data), HTTPStatus.OK.value
    elif request.method == 'POST':
        #load data from request
        request_data = json.loads(request.get_data().decode('UTF-8'))
        if request.get_data().decode('UTF-8') is None:
            abort(400)
        #items existence test
        ifItemExist = bool(db_managing.getItemId("songs", request_data["song_name"]))
        #if not exist
        if ifItemExist == False:
            #put item into data base
            db_managing.postItem('songs', request_data)
            #ask db for album_id
            album_id = db_managing.getItemId('albums' , album_name)
            #ask db for new song_id
            song_id = db_managing.getItemId('songs' , request_data["song_name"])
            #post album_id and song_id to linking table album_song
            db_managing.postItem('album_song',{"album_id": album_id, "song_id": song_id})
            return render_template("index.html", title='albums page', data=['Item added successfully']), HTTPStatus.CREATED.value
        #if item exists
        elif ifItemExist == True:
            return render_template("index.html", title='albums page', data=['Item already exists!']), HTTPStatus.CONFLICT.value
        return 'OK'


@app.route('/artists/<artist_name>/albums/<album_name>/songs/<song_name>', methods=['GET', 'PUT', 'DELETE'])
def current_songs_current_album(artist_name, album_name, song_name):
    if request.method == 'GET':
        current_song_data = JSONconverter.getJSONFromList(
            db_managing.getSongForAlbum(artist_name, album_name, song_name))
        translated_text = translator.getTranslation(
              db_managing.getCurrentText(artist_name, song_name)[0][0], 'en', 'ru')
        return render_template("index.html", title='current album page', data=current_song_data, translated=translated_text), HTTPStatus.OK.value
    elif request.method == 'PUT':
        #ask for request data
        request_data = json.loads(request.get_data().decode('UTF-8'))
        #ask for item id in an existing database
        item_id = db_managing.getItemId('songs' , request_data['song_name'])
        #items existence test
        ifItemExist = bool(item_id)
        #if items already exist
        if ifItemExist == True:
            #add to current data id
            request_data['song_id'] = item_id
            #put into data base with new data
            db_managing.updateItem('songs', request_data)
            #Informing the user about changes
            return render_template("index.html", title='current song page', data=['Item updated successfully']), HTTPStatus.OK.value
        #if item doesn't exist
        elif ifItemExist == False:
            #Informing the user about changes
            return render_template("index.html", title='current song page', data=['Item not found!']), HTTPStatus.NOT_FOUND.value
    elif request.method == 'DELETE':
        request_data = json.loads(request.get_data().decode('UTF-8'))
        item_id = db_managing.getItemId('songs' , request_data['song_name'])
        ifItemExist = bool(item_id)
        if ifItemExist == True:
            db_managing.deleteItem('songs', item_id)
            #delete song from linking table album_song
            db_managing.deleteItem('album_song', item_id, 'song')
            return render_template("index.html", title='current song page', data=['Item deleted successfully!']), HTTPStatus.ACCEPTED.value
        elif ifItemExist == False:
            return render_template("index.html", title='current song page', data=['Item not found!']), HTTPStatus.NOT_FOUND.value


@app.route('/search', methods=['GET'])
def search():
    if request.method == 'GET':
        args = request.args
        args_dict = args.to_dict()
        searched_data = JSONconverter.getJSONFromList(
            db_managing.searchItems(args_dict["table"], args_dict["item"]))
        return render_template("index.html", title='search page', data=searched_data), 200


@app.errorhandler(409)
def conflict(e):
    return jsonify({'errorCode': 409, 'message': 'Conflict'})


@app.errorhandler(404)
def not_found(e):
    return jsonify({'errorCode': f'{HTTPStatus.NOT_FOUND.value}', 'message': f'{HTTPStatus.NOT_FOUND.description}'})


@app.errorhandler(500)
def server_error(e):
    return jsonify({'errorCode': f'{HTTPStatus.INTERNAL_SERVER_ERROR.value}', 'message': f'{HTTPStatus.INTERNAL_SERVER_ERROR.description}'})


if __name__ == '__main__':
    app.run()
