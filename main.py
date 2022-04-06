from flask import Flask, request

from src import db_managing
from src import JSONconverter
from src import translator

app = Flask(__name__)


@app.route('/')
def show_home_page():
    return '<p>Home page</p>'

@app.route('/artists')
def show_all_artists():
    artists_data = JSONconverter.getJSONFromList(db_managing.getItems('artists'))
    return f'''
    <p>All artists:</p>
    <p>{artists_data}</p>
    '''

@app.route('/artists/<artist_name>')
def show_current_artist(artist_name):
    current_artist_data = JSONconverter.getJSONFromList(db_managing.getItems('artists', artist_name))
    return f'<p>Current artist: {current_artist_data}</p>'


@app.route('/artists/<artist_name>/songs')
def show_all_songs(artist_name):
    all_songs_data = JSONconverter.getJSONFromList(db_managing.getSongsForArtist(artist_name))
    return f'<p>Current artist all songs: {all_songs_data}</p>'


@app.route('/artists/<artist_name>/songs/<song_name>')
def show_current_song(artist_name, song_name):
    current_song_data = JSONconverter.getJSONFromList(db_managing.getCurrentSongForArtist(artist_name, song_name))
    translated_current_song_text = translator.getTranslation(db_managing.getCurrentTextSongForArtist(artist_name, song_name)[0][0], 'en', 'ru')
    return f'''
    <p>Current song current artist: {current_song_data}</p>
    <p>Translated text(en -> ru)</p>
    <p>{translated_current_song_text}</p>
    '''
    

@app.route('/artists/<artist_name>/albums')
def show_all_albums(artist_name):
    all_albums_data = JSONconverter.getJSONFromList(db_managing.getAlbumsForArtist(artist_name))
    return f'<p>All albums current artist: {all_albums_data}</p>'


@app.route('/artists/<artist_name>/albums/<album_name>')
def show_current_album(artist_name, album_name):
    current_album_data = JSONconverter.getJSONFromList(db_managing.getCurrentAlbumForAlbumsForArtist(artist_name, album_name))
    return f'<p>Current artist: {current_album_data}</p>'

@app.route('/search', methods=['GET'])
def search():
    args = request.args
    args_dict = args.to_dict()
    return f'''
    <p>Search item: {args_dict["item"]} in table {args_dict["table"]}</p>
    <p>{JSONconverter.getJSONFromList(db_managing.searchItems(args_dict["table"], args_dict["item"]))}</p>
    '''

if __name__ == '__main__':
    app.run()