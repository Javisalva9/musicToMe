import sys, deezer

client = deezer.Client()
obj_id = sys.argv[1]
song_search = []
try:
	song_list = client.get_playlist(obj_id).tracks
	for song in song_list:
		title = song.title
		artist = song.get_artist().name
		song_search.append((title + " " + artist).encode('utf8'))	
	for song_query in song_search:
		print song_query
except:
	print("Incorrect or null ID. Example: python api_deezer.py 908622995")
