import urllib2
import json


sc_client_id = 'a0b4638bae6d50a9296f7fc3f35442eb'
lastfm_api_key = "c43db4e93f7608bb10d96fa5f69a74a1"


def get_lastfm_artists(username, number):
		
		limit = number
		url = "http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user="+username+"&api_key="+lastfm_api_key+"&format=json&limit="+str(limit)
		print url
		data = urllib2.urlopen(url)
		data = json.load(data)
		artists = []
		for artist in data["topartists"]["artist"]:
			artists.append({"name":artist["name"], "artist_id":artist['mbid']})
		return artists


def lastfmAlbumTracklist(artist, title):
	artist = urllib.quote_plus(artist)
	title = urllib.quote_plus(title)

	url = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=c43db4e93f7608bb10d96fa5f69a74a1&artist="+artist+"&album="+title+"&autocomplete=1&format=json"
	print "This is the get album tracks URL " + url
	data = urllib2.urlopen(url)
	api_results = json.load(data)
	tracks = []
	for track in api_results['album']['tracks']['track']:
		artist = track['artist']['name']
		title = track['name']
		track_id = track['mbid']
		tracks.append({'artist':artist, 'title':title, 'track_id':track_id})
	# results = {'reid':reid, 'tracks':tracks}
	return tracks



def getSoundcloudUserFollow(username, limit, offset):
	names = []
	while True:
		url = 'http://api.soundcloud.com/users/'+username+'/followings.json?client_id='+sc_client_id+'&limit='+str(limit)+'&offset='+str(offset)
		print "Soundcloud API url: " + url
		data = urllib2.urlopen(url)
		api_results = json.load(data)
		for entry in api_results:
			name = entry['username']
			names.append(name)
		if len(api_results) < limit:
			break
		else:
			offset += limit
	return names