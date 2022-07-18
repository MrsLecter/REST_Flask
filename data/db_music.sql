select songs.song_year, songs.song_name, artists.artist_name
from songs
join artist_song_album on artist_song_album.song_id = songs.song_id
join artists on artist_song_album.artist_id = artists.artist_id
where songs.song_year between 1965 and 1978 order by songs.song_year desc
