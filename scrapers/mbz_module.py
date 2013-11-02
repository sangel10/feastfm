
import urllib
import urllib2
import json
import musicbrainzngs as mbz
# from scrapers.db_handler import check_if_follows

mbz.set_useragent("feast", "0.0.0", "santiagoangel10@gmail.com")





def urlToJson(url):
	data = urllib2.urlopen(url)
	api_results = json.load(data)
	return api_results



def getLabelReleases(mbid, rgids=None):
	if rgids == None:
		rgids = []
	releases, rgids = get_browse_releases('label', mbid, rgids)
	return releases, rgids

def getArtistReleases(mbid, rgids=None):
	if rgids == None:
		rgids = []
	releases, rgids = get_browse_releases('artist', mbid, rgids)
	return releases, rgids

def getReleasesByQuery(query, rgids=None):
	if rgids == None:
		rgids = []
	releases, rgids = get_browse_releases('stream', query, rgids)
	return releases, rgids


def getArtistByID(mbid):
	results = mbz.get_artist_by_id(mbid)
	artist = {'name':results['artist']['name'], 'artist_id':results['artist']['id']}
	return artist

def getLabelByID(mbid):
	results = mbz.get_label_by_id(mbid)
	label = {'name':results['label']['name'],'label_id':results['label']['id']}
	return label

def getReleaseByID(mbid):
	results = mbz.get_release_by_id(mbid ,includes = ["artist-credits"])
	release = {'title':results['release']['title'], 'reid':results['release']['id']}

	artists = []
	for entry in results['release']['artist-credit']:
		try:
			artist = {'artist_name':entry['artist']['name'], 'artist_id':entry['artist']['id']}
			artists.append(artist)
		except:
			continue
	release['artists'] = artists
	print "getReleaseByID returns:"
	print release
	return release

def getRecordingByID(mbid):
	results = mbz.get_recording_by_id(mbid, includes=["artist-credits"])

	artists = []
	for entry in results['recording']['artist-credit']:
		try:
			artist = {'artist_name':entry['artist']['name'], 'artist_id':entry['artist']['id']}
			artists.append(artist)
		except:
			continue

	recording = {'title':results['recording']['title'], 'mbid':results['recording']['id'], 'artists':artists}	
	return recording 








def get_browse_releases(query_type, mbid_or_query, rgids = None):
	offset = 0
	releases = []
	if rgids == None:
		rgids = []
	# while True:
	while offset <= 1000:
		if query_type == 'label':
			url = "http://www.musicbrainz.org/ws/2/release?label="+mbid_or_query+"&fmt=json&limit=100&offset="+str(offset)+"&inc=artist-credits+release-groups+labels"
		if query_type == 'artist':
			url = "http://www.musicbrainz.org/ws/2/release?artist="+mbid_or_query+"&fmt=json&limit=100&offset="+str(offset)+"&inc=artist-credits+release-groups+labels"
		if query_type == 'stream':
			url = "http://www.musicbrainz.org/ws/2/release?&query="+mbid_or_query+ "&limit=100&fmt=json&offset="+str(offset)
		print "THIS IS THE QUERY URL for get_browse_releases: \n" + url
		data = urllib2.urlopen(url)
		api_results = json.load(data)
		if api_results["releases"] == []:
			break
		parsed_results = parse_releases(api_results, rgids)
		releases += parsed_results['releases']
		rgids += parsed_results['rgids']
		offset +=100
	#return render_to_response('scrapers/home.html',{'page':query_type, 'releases':releases})
	# releases = check_if_follows('artists', releases)
	# releases = check_if_follows('labels', releases)
	return releases, rgids



def parse_releases(api_results, rgids):
	releases = []
	for release in api_results['releases']:
		rgid = release['release-group']['id']
		if rgid in rgids:
			continue
		try: 
			date = release['date']
		except:
			date = ""
		title = release['title']
		artist = release['artist-credit'][0]['artist']['name']
		artist_id = release['artist-credit'][0]['artist']['id']
		reid = release['id']
		# cat_num = release['label-info'][0]['catalog-number']
		try:
			primary_type = release['release-group']['primary-type']
		except:
			primary_type = ""
		try:
			secondary_types = release['release-group']['secondary-types']
		except:
			secondary_types = ""
		try:
			label = release['label-info'][0]['label']['name']
			label_id = release['label-info'][0]['label']['id']
			cat_num = release['label-info'][0]['catalog-number']
		except:
			label = ""
			label_id = ""
			cat_num = ""
		rgids.append(rgid)
		releases.append({
			'date':date,
			'title':title,
			'artist':artist,
			'artist_id':artist_id,
			'rgid':rgid,
			'reid':reid,
			'cat_num':cat_num,
			'primary_type':primary_type,
			'secondary_types':secondary_types,
			'label':label,
			'label_id':label_id,
			})
	return {'releases':releases, 'rgids':rgids}




def mbz_search(query, query_type, limit =100):
	url = "http://musicbrainz.org/ws/2/"+query_type+"/?query="+query+"&fmt=json&limit="+str(limit)
	print "QUERY URL: " + url
	data = urllib2.urlopen(url)
	api_results = json.load(data)
	#print api_results
	return api_results


def get_english_alias(lookup_type, mbid):
	url = "http://musicbrainz.org/ws/2/"+lookup_type+"/"+mbid+"?inc=aliases&fmt=json"
	data = urllib2.urlopen(url)
	results = json.load(data)
	name = ""
	for alias in results['aliases']:
		if alias['locale'] == "en":
			name = alias['name']
			break
	if not name:
		name = results['name']
	return name


def getTracklistByReid(reid):

	url = "http://www.musicbrainz.org/ws/2/release/"+reid+"?fmt=json&inc=artist-credits+recordings"
	print "This is the get album tracks URL " + url
	data = urllib2.urlopen(url)
	api_results = json.load(data)
	tracks = []
	for entry in api_results['media']:
		for track in entry['tracks']:
			artist = track['artist-credit'][0]['name']
			artist_id = track['artist-credit'][0]['artist']['id']
			title = track['recording']['title']
			track_id = track['recording']['id']
			tracks.append({'artist':artist, 'title':title, 'track_id':track_id, 'artist_id':artist_id})
	return tracks 
	# results = {'reid':reid, 'tracks':tracks}



# The following are notes from Omid on different systems of advancing the way the MBZ data is retrieved/*
#   MusicBrainzArtist : Hash { name : String, id -> Integer}

# */

# class MusicBrainsPythonWrapper """ What you're tempted to do, but no immediate gain. Aesthetical reason.





# class MusicBrainzAPICached


# class MusicBrainzDB

# 	/*
# 		Takes bla of type bla
# 		returns foo of type bar

# 		!= leaky abstraction
# 	*/
# 	def getArtist(artistID) 
# 		returns 


# 	def getRelease(releaseID)



# 	..