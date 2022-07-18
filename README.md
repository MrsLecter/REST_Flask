## About

Simple REST API

## Technology

- cherrypy
- postgreSQL
- GoogleTranslator
- unittests

## Before running commands from the command line, you must:

- Install postgreSQL, cherrypy, json, deep_translator
- Clone a repository using git


## API path

* **GET** 
* '/artist' or '/artist/${artistName}' returns all atrists or artist with the required 'artistName';
* 'artist/{artistName}/song' returns all songs for current artist;
* 'artist/{artistName}/song/${songName}' returns required 'songName' for current 'artistName';
* 'artist/{artistName}/album' returns all albums for current 'artistName';
* 'artist/{artistName}/album/${albumName}' returns required 'albumName' for current 'artistName';
* 'artist/{artistName}/album/${albumName}/${songName} returns required 'songName' for current 'albumName' for current 'artistName';
* 'search?item=${itemName}&table={tableName}' returns required 'itemName'(artist, song, album) for current 'tableName'


## Artists and Songs are stored as objects that have following properties:
* id - unique identifier (`string`, `uuid`) generated on server side;
* artist_name
* album_name, album_year, album_info
* song_name, song_text, song_year, origin_lang

## Output

-returns data in JSON

<h4>Downloading</h4>
<code>git clone {repository URL}</code>



