#!/usr/bin/python3
import json


def getDictFromList(listOfTuple):
    listOfDict = []
    keys_song = ['song_name',
                 'song_text', 'song_year', 'original_lang']
    keys_song_id = ['song_id', 'song_name',
                 'song_text', 'song_year', 'original_lang']
    keys_albums = ['album_name', 'album_year', 'album_info']
    keys_albums_id = ['album_id','album_name', 'album_year', 'album_info']
    keys_artist = ['artist_id', 'artist_name', 'artist_info']

    for list in listOfTuple:
        required_dict = {}
        # find required keys pattern by way calculated length of input list
        if len(list) == 5 and type(list[0]) == type(1):
            for j in range(len(list)):
                required_dict[keys_song_id[j]] = list[j]
        elif len(list) == 4 and type(list[0]) != type(1):
            for j in range(len(list)):
                required_dict[keys_song[j]] = list[j]
        elif len(list) == 4 and type(list[0]) == type(1):
            for j in range(len(list)):
                required_dict[keys_albums_id[j]] = list[j]
        elif len(list) == 3 and type(list[0]) != type(1):
            for j in range(len(list)):
                required_dict[keys_albums[j]] = list[j]
        elif len(list) == 3:
            for j in range(len(list)):
                required_dict[keys_artist[j]] = list[j]
        listOfDict.append(required_dict)
    return listOfDict

#return dict
def getJSONFromList(listOfTuple):
    # give list dict from list
    required_dict = getDictFromList(listOfTuple)
    # use json library to receive valid json
    return json.loads(json.dumps(required_dict))
