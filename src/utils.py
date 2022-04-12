from src import db_managing


def deleteWithRelatedElements(item_name, item_id):
    related_item = db_managing.getItems('artist_song_album',  item_name, item_id )

    if item_name == 'album':
        db_managing.deleteItem('artist_song_album',item_id , item_name)
        db_managing.deleteItem('albums', item_id)
    elif item_name == 'song':
        print(item_id, item_name)
        db_managing.deleteItem('artist_song_album', item_id, item_name)
        db_managing.deleteItem('songs', item_id)
    elif item_name == 'artist':
        songs_id = []
        albums_id = []
        for item in related_item:
            songs_id.append(item[1])
            albums_id.append(item[2])

        db_managing.deleteItem('artist_song_album', item_id ,item_name )

        deleteElementsList(songs_id, 'songs')
        deleteElementsList(albums_id, 'albums')
        db_managing.deleteItem('artists', item_id)
    
def deleteElementsList(required_list, table_name):
    for id in required_list:
        db_managing.deleteItem(table_name, id)
