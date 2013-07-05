import datetime
import urllib2
import json
from scrapers.models import *

today.strftime('%Y-%m-%d')
last_month.strftime('%Y-%m-%d')



releases_query = "https://musicbrainz.org/search?query=date%3A%5B2013-05-14+TO+2013-05-21%5D&type=release&limit=25&method=advanced"

lucine_query = "date:[2013-05-21 TO 2013-05-21]"

def get_mbz_releases():
	today = datetime.date.today()
	last_month = today - datetime.timedelta(days=30)
	end_date = today.strftime('%Y-%m-%d')
	start_date = last_month.strftime('%Y-%m-%d')
	offset = 0
	url = "http://www.musicbrainz.org/ws/2/release?&query=date:["+start_date+"%20TO%20"+end_date+"]&limit=100&fmt=json&offset="+str(offset)
	data = urllib2.urlopen(url)
	api_results = json.load(data)
	return api_results["releases"]



def filter_releases():
	artist_set = Artist.objects.all()
	label_set = Label.objects.all()
	release_group_set = Release_group.objects.all()
	mbz_release_set = mbz_release.objects.all()
	# evaluates entire query_set and caches it
	bool(artist_set)
	bool(label_set)
	bool(release_group_set)
	bool(mbz_release_set)
	releases = get_mbz_releases()

	for release in releases:
		if release['status'] == 'Official':
			if artist_set.filter(name__iexact = release["artist"]) or label_set.filter(name__iexact = release["label"]):
				if "id" in release:
					mbz_reid = release["id"]
				else:
					mbz_reid = ""
				# if the release ID is already in the DB, move on to the next release
				# if its not continue doing everything else
				if mbz_reid and mbz_release_set.filter(mbz_reid = mbz_reid):
					continue
				else:
					try:
						mbz_rgid = release["release-group"]["id"]
					except:
						mbz_rgid = ""
						print "no release-Group ID"
					if mbz_rgid and release_group_set.filter(mbz_rgid = mbz_rgid):
						release_group = release_group_set.filter(mbz_rgid = mbz_rgid)[0]
						mbz_release = save_release(release)
						if mbz_release:
							release_group.mbz_release.add(mbz_release)
							release_group.save()
						tracks = []
						release = releases_lookup(mbz_reid)
						for medium in release['media']:
							for entry in medium['tracks']:
								track = save_release_track(track)
								if track:
									tracks.append(track)
						for track in tracks:
							release_group.sounds.add(track)

						add tracks to DB
						add tracks to RG
					elif mbz_rgid:
						new RG
						new mbz_release
						new tracks
					else:
						pass

def releases_lookup(reid):
	url = "http://www.musicbrainz.org/ws/2/release/"+reid+"?fmt=json&inc=artist-credits+recordings"
	data = urllib2.urlopen(url)
	release = json.load(data)
	return release

#accepts release
def save_release(release):
	mbz_release = mbz_release(mbz_reid = mbz_reid)
	mbz_release.save()
	try:
		cat_num = release["label-info"]['catalog-number']
		mbz_release.mbz_catalog_number = cat_num
		mbz_release.save()
	else:
		pass
	return mbz_release

def save_release_track(track):
	artists = []
	for entry in track['artist-credit']:
		artist = entry['name']
		artists.append(artist)
	for artist in artists:
		sound = Sound.artists.add(artist)
	title = track['title']
	if "length" in track:
		length = track['length']
		sound.length = length
	mbz_id = track['recording']['id']
	sound.title = title
	sound.mbz_id = mbz_id
	sound.save()
	return sound


def save_release_group_tracks():
	pass

def add_release_group():
	release = Release(rgid = mbz_rgid)
	try:
		artist = Artist.get()
	except:
		artist = Artist.(name = recording)

def add_release():
	pass

def add_tracklist():
	if songs exist:
		associate them with release
	else:
		add new songs
		associate them with release




# gets all labels for artist
			if artist_set.filter(name__iexact = release["artist"]):
				get all recordings by artist
				for recording in recordings:
					if recording['label'] in label_set:
						associate wtih RG\
					else:
						create label
						associate with RG
				add_artist_labels()
			else:
				add artist
			if label_set.filter(name__iexact = release["label"]):
				add_label_artists()
			else:
				add label


			release_info = get_mbz_release_info(release)



def save_new_release():

	artist
	label 
	mbz_rgid

	find official release with longest tracklist
		add all tracks in order
			save tracks
			create relation with release
		get all tracks from rgid
			add those tracks as extras

	for all mbz_releases:
		save_mbz_releases
		save_catalog numbers
		create relation with release




	


	create mbz_reid entry
		mbz_reid
		catalog number
	save it in DB

	look at all songs
		add any that dont already exist
	create relation to rgid
	create relation btwn rgid and label

def save_tracks():
	RELEASE group

	artist
	title
	release group and track number
	mbz_song_id
	length
	source



def add_artist_labels:
	pass
def add_label_artists:
	pass

def get_mbz_release_info(release):
	try:
		rgid = release['release-group']['id']
	else:
		print "Couldn't get release-group ID"
		rgid = ""
		pass
	labels = []
	try:
		label =


	return api_results


	#if artist or label exists in DB
def get_all_from_release_group(rgid):
	url = "http://www.musicbrainz.org/ws/2/release?&query=rgid:"+rgid+"&limit=100&fmt=json&offset=0"
	data = urllib2.urlopen(url)
	api_results = json.load(data)
	for release in api_results["releases"]:
		if release["status"] == "Official" and release["score"] = 100:

			get_musicbrainz_album_info(release)




def get_musicbrainz_album_info(release):
	new_JSON
	JSON_to_data = {"['id']":"mb_release_id", '["title"]':"album_title", '["date"]':"release_date"}

	if "id" in release:
		mb_release_id = release["id"]
	else: 
		mb_release_id = ""
	if "title" in release:
		album_name = release["title"]
	else:
		album_name = ""
	if "date" in release:
		release_date = release["date"]
	else:
		release_date = None

	try:
		mb_release_group_id = release["release-group"]["id"]
	except:
		print "No release group"
		pass


	album_artists = []
	try:
		for entry in release["artist-credit"]:
			album_artist = entry["artist"]["name"]
			album_artists.append(album_artist)
	except E: 
		print "No artist name"
		pass

	labels = []
	try:
		for entry in release["label-info"]:
			label = entry["label"]["name"]
			labels.append(label)
	except e:
		print "no label name"
		pass



	if release["id"]:
		mb_release_id = release["id"]
	else: 
		mb_release_id = ""
	if release["title"]:
		album_name = release["title"]
	else:
		album_name = ""
	if release["date"]:
		release_date = release["date"]
	else:
		release_date = None
	album_artists = []
	if release["artist-credit"]:
		for entry in release["artist-credit"]:
			if entry["artist"]["name"]:
				artist = entry["artist"]["name"]
				album_artists.append(artist)
	labels = []
	catalog_ids = []
	if release["label-info"]:
		for entry in release["label-info"]:
			if "label" in entry:
				if "name" in entry["label"]:
					label = entry["label"]["name"]
					labels.append(label)
			if "catalog-number" in entry:
				catalog_id = entry["catalog-number"]
				catalog_ids.append(catalog_id)
	tracks = get_musicbrainz_album_tracks(mb_release_id)
	return {"mb_release_id":mb_release_id, "album_name":album_name, "album_artists":album_artists, 
	"release_date":release_date, "labels":labels, "catalog_ids":catalog_ids, "tracks":tracks}


def clean_release_JSON(release):
	if "id" not in release:
		release["id"] = ""
	if "title" not in release:
		release["title"] = ""
	if "date" not in release:
		release["date"] = None

	if "artist-credit" not in release:
		release["artist-credit"] = {"artist":{"name":""}}

	elif "artist" not in release["artist-credit"]:
		release["artist-credit"]["artist"] = {"name":""}

	elif "name" not in release["artist-credit"]["artist"]:
		release["artist-credit"]["artist"]["name"] = ""

		for entry in release["artist-credit"]:
			if entry["artist"]["name"]:
				artist = entry["artist"]["name"]
				album_artists.append(artist)

	if "label-info" not in release:
		release["label-info"] = []
	elif !release["label-info"]
		for entry in release["label-info"]:
			if "label" in entry:
				if "name" in entry["label"]:
					label = entry["label"]["name"]
					labels.append(label)
			if "catalog-number" in entry:
				catalog_id = entry["catalog-number"]
				catalog_ids.append(catalog_id)


def get_musicbrainz_album_tracks(mbid):
	url = "http://www.musicbrainz.org/ws/2/release/"+mbid+"?fmt=json&inc=recordings"
	data = urllib2.urlopen(url)
	api_results = json.load(data)
	tracks = []
	#return api_results
	for entry in api_results["media"][0]["tracks"]:
		length = entry["length"]
		title = entry["title"]
		mbz_song_id = entry["recording"]["id"]
		track_number = entry["number"]
		track_artist = get_musicbrainz_track_artist(mb_song_id)
		tracks.append({"title":title, "length":length, "mbz_song_id":mbz_song_id, "track_number":track_number})
	return tracks

def get_musicbrainz_track_artist(mbid):
	url = "http://www.musicbrainz.org/ws/2/recording/"+mbid+"?fmt=json&inc=artists"
	data = urllib2.urlopen(url)
	api_results = json.load(data)
	artist = api_results["artist-credit"][0]["artist"]["name"]
	return artist 


release = "e3563aa1-7570-4d2d-9aa7-d1f18562b782"

