#!/usr/bin/python3
import psycopg2
from configparser import ConfigParser


# configure server
def config(filename='database.ini', section='postgresql'):
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


# get items from db
def getItems(table_name, item_name='none'):
    requested_data = []
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        if table_name == 'artists':
            if item_name == 'none':
                cur.execute("SELECT * FROM artists ORDER BY artist_name")
            else:
                cur.execute(
                    f"select * from artists where artist_name='{item_name}'")
            print(cur.rowcount)
        elif table_name == 'songs':
            if item_name== 'none':
                cur.execute("SELECT * FROM songs ORDER BY song_name")
            else:
                cur.execute(
                    f"SELECT * FROM songs WHERE song_name='{item_name}'")
            print(cur.rowcount)
        elif table_name == 'albums':
            if item_name == 'none':
                cur.execute("SELECT * FROM albums ORDER BY album_name")
            else:
                cur.execute(
                    f"SELECT * FROM albums WHERE album_name='{item_name}'")
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


# post items to db
def postItem(table_name, item_object):
    requested_data = None
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        if table_name == 'artists':
            cur.execute(
                f"insert into {table_name} values(DEFAULT, '{item_object['name']}','{item_object['info']}')")
        elif table_name == 'songs':
            cur.execute(
                f"insert into {table_name} values(DEFAULT, '{item_object['name']}','{item_object['text']}','{item_object['year']}', '{item_object['lang']}')")
        elif table_name == 'albums':
            cur.execute(
                f"insert into {table_name} values(DEFAULT, '{item_object['name']}','{item_object['year']}','{item_object['info']}')")

        requested_data = cur.rowcount
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return requested_data


# search items on db in current table
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


# delete item from db
def deleteItem(table_name, item_id):
    requested_data = None
    conn = None
    rows_deleted = 0
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(
            f"DELETE FROM {table_name} WHERE {table_name[:-1]}_id = {item_id}")
        print(cur.rowcount)
        rows_deleted = cur.rowcount
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows_deleted


# update db item
def updateItem(table_name, item_object):
    conn = None
    updated_rows = 0
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        if table_name == 'artists':
            cur.execute(
                f"UPDATE {table_name} SET {table_name[:-1]}_name='{item_object['name']}', {table_name[:-1]}_info='{item_object['info']}' WHERE {table_name[:-1]}_id={item_object['id']}")
        elif table_name == 'songs':
            cur.execute(
                f"UPDATE {table_name} SET {table_name[:-1]}_name='{item_object['name']}', {table_name[:-1]}_text='{item_object['text']}', {table_name[:-1]}_year='{item_object['year']}', original_lang='{item_object['lang']}' WHERE {table_name[:-1]}_id={item_object['id']}")
        elif table_name == 'albums':
            cur.execute(
                f"UPDATE {table_name} SET {table_name[:-1]}_name='{item_object['name']}', {table_name[:-1]}_year='{item_object['year']}', {table_name[:-1]}_info='{item_object['info']}' WHERE {table_name[:-1]}_id={item_object['id']}")
        updated_rows = cur.rowcount
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return updated_rows


def getSongsForArtist(artist_name):
    requested_data = []
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        cur.execute(f'''select distinct song_name, song_text, song_year, original_lang from songs
                    join artist_song_album
                    on songs.song_id=artist_song_album.song_id
                    join artists
                    on artist_song_album.album_id=artists.artist_id
                    where artists.artist_name='{artist_name}'
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


def getAlbumsForArtist(artist_name):
    requested_data = []
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        cur.execute(f'''select distinct album_name, album_year, album_info from albums
                        join artist_song_album
                        on albums.album_id = artist_song_album.album_id
                        join artists
                        on artist_song_album.artist_id = artists.artist_id
                        where artists.artist_name = '{artist_name}'
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


def getCurrentAlbumForAlbumsForArtist(artist_name, album_name):
    requested_data = []
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        cur.execute(f'''select distinct album_name, album_year, album_info from albums
                        join artist_song_album
                        on albums.album_id = artist_song_album.album_id
                        join artists
                        on artist_song_album.artist_id = artists.artist_id
                        where artists.artist_name = '{artist_name}' and albums.album_name='{album_name}'
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


def getSongsForAlbumsForArtist(album_name, artist_name):
    requested_data = []
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        cur.execute(f'''select distinct song_id, song_name, song_text, song_year, original_lang from songs
                        join artist_song_album 
                        on songs.song_id = artist_song_album.song_id
                        join albums
                        on artist_song_album.album_id = albums.album_id
                        join artists
                        on artist_song_album.artist_id = artists.artist_id
                        where artists.artist_name = '{artist_name}' and albums.album_name = '{album_name}'
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

def getCurrentSongForArtist(artist_name, song_name):
    requested_data = []
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        cur.execute(f'''select distinct song_name, song_text, song_year, original_lang from songs
                        join artist_song_album 
                        on songs.song_id = artist_song_album.song_id
                        join albums
                        on artist_song_album.album_id = albums.album_id
                        join artists
                        on artist_song_album.artist_id = artists.artist_id
                        where artists.artist_name = '{artist_name}' and songs.song_name='{song_name}'
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


def getCurrentTextSongForArtist(artist_name, song_name):
    requested_data = []
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        cur.execute(f'''select distinct song_text from songs
                        join artist_song_album 
                        on songs.song_id = artist_song_album.song_id
                        join albums
                        on artist_song_album.album_id = albums.album_id
                        join artists
                        on artist_song_album.artist_id = artists.artist_id
                        where artists.artist_name = '{artist_name}' and songs.song_name='{song_name}'
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


