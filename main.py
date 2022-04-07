from flask import Flask, request, render_template

from src import db_managing
from src import JSONconverter
from src import translator

app = Flask(__name__)


@app.route('/')
def show_home_page():
    return render_template("index.html", title='home page', data={'hello world'})


@app.route('/artists')
def show_all_artists():
    artists_data = JSONconverter.getJSONFromList(
        db_managing.getItems('artists'))
    return render_template("index.html", title='artists page', data=artists_data)


@app.route('/artists/<artist_name>')
def show_current_artist(artist_name):
    current_artist_data = JSONconverter.getJSONFromList(
        db_managing.getItems('artists', artist_name))
    return render_template("index.html", title='current artists page', data=current_artist_data)


@app.route('/artists/<artist_name>/songs')
def show_all_songs(artist_name):
    all_songs_data = JSONconverter.getJSONFromList(
        db_managing.getSongsForArtist(artist_name))
    return render_template("index.html", title='all songs page', data=all_songs_data)


@app.route('/artists/<artist_name>/songs/<song_name>')
def show_current_song(artist_name, song_name):
    current_song_data = JSONconverter.getJSONFromList(
        db_managing.getCurrentSongForArtist(artist_name, song_name))
    translated_current_song_text = translator.getTranslation(
        db_managing.getCurrentTextSongForArtist(artist_name, song_name)[0][0], 'en', 'ru')
    return render_template("index.html", title='current song page', data=current_song_data, translated=translated_current_song_text)


@app.route('/artists/<artist_name>/albums')
def show_all_albums(artist_name):
    all_albums_data = JSONconverter.getJSONFromList(
        db_managing.getAlbumsForArtist(artist_name))
    return render_template("index.html", title='all albums page', data=all_albums_data)


@app.route('/artists/<artist_name>/albums/<album_name>')
def show_current_album(artist_name, album_name):
    current_album_data = JSONconverter.getJSONFromList(
        db_managing.getCurrentAlbumForAlbumsForArtist(artist_name, album_name))
    return render_template("index.html", title='current album page', data=current_album_data)


@app.route('/search', methods=['GET'])
def search():
    args = request.args
    args_dict = args.to_dict()
    searched_data = JSONconverter.getJSONFromList(
        db_managing.searchItems(args_dict["table"], args_dict["item"]))
    return render_template("index.html", title='search page', data=searched_data)


if __name__ == '__main__':
    app.run()
