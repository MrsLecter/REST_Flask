#!/usr/bin/python3
import typing
from typing import Dict
import psycopg2
from configparser import ConfigParser


# configure server
def config(filename: str='database.ini', section: str='postgresql') -> Dict:
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} not found in the {1} file'.format(section, filename))
    return db


# test query to postgresql server
def connect():
    conn = None
    try:
        # read connection parameters
        params = config()
        print('Connecting to the PostgreSQL database...')
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        print('PostgreSQL database version:')
        # execute a statement
        cur.execute('SELECT version()')
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def getItems(table_name, item_name='none', item_id='none'):
    requested_data = []
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        if table_name == 'artists' or table_name == 'songs' or table_name == 'albums':
            if item_name == 'none':
                cur.execute(
                    f"SELECT * FROM {table_name}")
            else:
                cur.execute(
                    f"SELECT * FROM {table_name} WHERE {table_name[:-1]}_name='{item_name}'")
        elif table_name == 'artist_album':
            cur.execute(
                f"SELECT * FROM {table_name} WHERE {item_name}_id='{item_id}'")
        elif table_name == 'album_song':
            cur.execute(
                f"SELECT * FROM {table_name} WHERE {item_name}_id='{item_id}'")

        row = cur.fetchone()
        while row is not None:
            requested_data.append(row)
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return requested_data


def postItem(table_name, item_object):
    requested_data = None
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        if table_name == 'artists':
            cur.execute(
                f"insert into {table_name} values(DEFAULT, '{item_object['artist_name']}','{item_object['artist_info']}')")
        elif table_name == 'songs':
            cur.execute(
                f"insert into {table_name} values(DEFAULT, '{item_object['song_name']}','{item_object['song_text']}','{item_object['song_year']}', '{item_object['original_lang']}')")
        elif table_name == 'albums':
            cur.execute(
                f"insert into {table_name} values(DEFAULT, '{item_object['album_name']}','{item_object['album_year']}','{item_object['album_info']}')")
        elif table_name == 'artist_album':
            cur.execute(
                f"insert into {table_name} values('{item_object['artist_id']}', '{item_object['album_id']}')")
        elif table_name == 'album_song':
            cur.execute(
                f"insert into {table_name} values('{item_object['album_id']}', '{item_object['song_id']}')")
        requested_data = cur.rowcount
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return requested_data


def searchItems(table_name, item_name):
    requested_data = None
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        cur.execute(
            f"SELECT * FROM {table_name} WHERE {table_name[:-1]}_name LIKE('{item_name}')")
        cur.execute(
            f"SELECT * FROM {table_name} WHERE {table_name[:-1]}_name LIKE('{item_name[:int(len(item_name)/2)]}%')")
        cur.execute(
            f"SELECT * FROM {table_name} WHERE {table_name[:-1]}_name LIKE('%{item_name[int(len(item_name)/2):]}')")

        row = cur.fetchall()
        while row is not None:
            requested_data = row
            row = cur.fetchone()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return requested_data


def deleteItem(table_name, item_id, item_name='none'):
    conn = None
    rows_deleted = 0
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        if table_name == 'artists' or table_name == 'songs' or table_name == 'albums':
            cur.execute(
                f"DELETE FROM {table_name} WHERE {table_name[:-1]}_id = {item_id}")
        elif table_name == 'artist_album':
            cur.execute(
                f"DELETE FROM {table_name} WHERE {item_name}_id = {item_id}")
        elif table_name == 'album_song':
            cur.execute(
                f"DELETE FROM {table_name} WHERE {item_name}_id = {item_id}")

        rows_deleted = cur.rowcount
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows_deleted


def updateItem(table_name, item_object):
    conn = None
    updated_rows = 0
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        if table_name == 'artists':
            cur.execute(
                f"UPDATE {table_name} SET {table_name[:-1]}_name='{item_object['artist_name']}', {table_name[:-1]}_info='{item_object['artist_info']}' WHERE {table_name[:-1]}_id={item_object['artist_id']}")
        elif table_name == 'songs':
            cur.execute(
                f"UPDATE {table_name} SET {table_name[:-1]}_name='{item_object['song_name']}', {table_name[:-1]}_text='{item_object['song_text']}', {table_name[:-1]}_year='{item_object['song_year']}', original_lang='{item_object['original_lang']}' WHERE {table_name[:-1]}_id={item_object['song_id']}")
        elif table_name == 'albums':
            cur.execute(
                f"UPDATE {table_name} SET {table_name[:-1]}_name='{item_object['album_name']}', {table_name[:-1]}_year='{item_object['album_year']}', {table_name[:-1]}_info='{item_object['album_info']}' WHERE {table_name[:-1]}_id={item_object['album_id']}")
        
        updated_rows = cur.rowcount
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return updated_rows


def getAlbumsForArtist(artist_name):
    requested_data = []
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        cur.execute(f'''SELECT DISTINCT album_name, album_year, album_info FROM albums
                        JOIN artist_album
                        ON albums.album_id = artist_album.album_id
                        JOIN artists
                        ON artists.artist_id = artist_album.artist_id
                        WHERE artists.artist_name = '{artist_name}'
                        ''')

        row = cur.fetchone()
        while row is not None:
            requested_data.append(row)
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return requested_data


def getCurrentAlbum(artist_name, album_name):
    requested_data = []
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        cur.execute(f'''SELECT DISTINCT album_name, album_year, album_info FROM albums
                        JOIN artist_album
                        ON albums.album_id = artist_album.album_id
                        JOIN artists
                        ON artist_album.artist_id = artists.artist_id
                        WHERE artists.artist_name = '{artist_name}' AND albums.album_name='{album_name}'
                        ''')

        row = cur.fetchone()
        while row is not None:
            requested_data.append(row)
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return requested_data


def getSongsForArtist(artist_name):
    requested_data = []
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        cur.execute(f'''SELECT DISTINCT song_name, song_text, song_year, original_lang FROM songs
                    JOIN album_song
                    ON songs.song_id=album_song.song_id
                    JOIN artist_album
                    on artist_album.album_id=album_song.album_id
                    JOIN artists
                    ON artists.artist_id=artist_album.artist_id
                    WHERE artists.artist_name='{artist_name}'
                    ''')

        row = cur.fetchone()
        while row is not None:
            requested_data.append(row)
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return requested_data


def getSongsForAlbums(artist_name, album_name):
    requested_data = []
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        cur.execute(f'''SELECT DISTINCT song_name, song_text, song_year, original_lang FROM songs
                        JOIN album_song 
                        ON songs.song_id = album_song.song_id
                        JOIN artist_album
                        ON artist_album.album_id = album_song.album_id
                        JOIN artists
                        ON artist_album.artist_id = artists.artist_id
                        JOIN albums
                        ON artist_album.album_id = albums.album_id
                        WHERE artists.artist_name = '{artist_name}' AND albums.album_name ='{album_name}'
                        ''')

        row = cur.fetchone()
        while row is not None:
            requested_data.append(row)
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return requested_data


def getSongForAlbum(artist_name, album_name, song_name):
    requested_data = []
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        cur.execute(f'''SELECT DISTINCT song_name, song_text, song_year, original_lang FROM songs
                        JOIN album_song 
                        ON songs.song_id = album_song.song_id
                        JOIN artist_album
                        ON artist_album.album_id = album_song.album_id
                        JOIN artists
                        ON artist_album.artist_id = artists.artist_id
                        JOIN albums
                        ON artist_album.album_id = albums.album_id
                        WHERE artists.artist_name = '{artist_name}' AND albums.album_name = '{album_name}'
                        AND songs.song_name = '{song_name}'
                        ''')

        row = cur.fetchone()
        while row is not None:
            requested_data.append(row)
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return requested_data


def getCurrentText(artist_name, song_name):
    requested_data = []
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        cur.execute(f'''SELECT DISTINCT song_text FROM songs
                        JOIN album_song
                        ON songs.song_id = album_song.song_id
                        JOIN albums
                        ON album_song.album_id = albums.album_id
                        JOIN artist_album
                        ON artist_album.album_id = albums.album_id
                        JOIN artists
                        ON artists.artist_id = artist_album.artist_id
                        WHERE artists.artist_name = '{artist_name}' AND songs.song_name='{song_name}'
                        ''')

        row = cur.fetchone()
        while row is not None:
            requested_data.append(row)
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return requested_data


def getAlbumForSong(artist_name, song_name):
    requested_data = []
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        cur.execute(f'''SELECT DISTINCT album_name FROM songs
                        JOIN album_song
                        ON songs.song_id = album_song.song_id
                        JOIN albums
                        ON album_song.album_id = albums.album_id
                        JOIN artist_album
                        ON artist_album.album_id = albums.album_id
                        JOIN artists
                        ON artists.artist_id = artist_album.artist_id
                        WHERE artists.artist_name = '{artist_name}' AND songs.song_name='{song_name}'
                        ''')

        row = cur.fetchone()
        while row is not None:
            requested_data.append(row)
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return requested_data


def getItemId(table_name, item_name):
    requested_data = None
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        if table_name == 'artists':
            cur.execute(
                f"SELECT artist_id FROM artists WHERE artist_name='{item_name}'")
        elif table_name == 'songs':
            cur.execute(
                f"SELECT song_id FROM songs WHERE song_name='{item_name}'")
        elif table_name == 'albums':
            cur.execute(
                f"SELECT album_id FROM albums WHERE album_name='{item_name}'")
        row = cur.fetchone()
        requested_data = 0 if row is None else row[0]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return requested_data


# if __name__ == '__main__':
#     print(getSongForAlbum(test_artist, test_album, test_song3))

