from django.http import HttpResponse
from django.shortcuts import render_to_response
import urllib2
import json
import urllib
import datetime
from django.template import RequestContext
import simplejson



from django.contrib.auth.decorators import login_required
from scrapers.models import *

import musicbrainzngs as mbz
from scrapers.mbz_module import *
from scrapers.db_handler import *

mbz.set_useragent("feast", "0.0.0", "santiagoangel10@gmail.com")

sc_client_id = 'a0b4638bae6d50a9296f7fc3f35442eb'
lastfm_api_key = "c43db4e93f7608bb10d96fa5f69a74a1"


#@login_required(login_url='/accounts/login/')
def home(request):
	if request.GET:
		get = request.GET.copy()
		username = get['username']
		artists = get_lastfm_artists(username, 100)
		artist_names = []
		for artist in artists:
			artist_names.append(artist['name'])	
		query = get_stream_query('artist', artist_names)

		releases, rgids = get_browse_releases('stream', query)


		#return HttpResponse("Username found: %s" % username )


		return render_to_response('scrapers/home.html',{'page':'home', 'releases':releases}, context_instance=RequestContext(request))
		#return render('scrapers/home.html',{'page':'home', 'releases':releases})


		# call username API
		# send to template that charts out each 
	else:
		#return HttpResponse("No username")

		return render_to_response('scrapers/home.html', {'page':'start'}, context_instance=RequestContext(request))
		#return render_to_response('scrapers/home.html', {'page':'start'}, context_instance=RequestContext(request))


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

def get_stream_query(query_type, mbids):
	# query_type = 'artist'
	today = datetime.date.today()
	last_month = today - datetime.timedelta(days=30)
	end_date = today.strftime('%Y-%m-%d')
	start_date = last_month.strftime('%Y-%m-%d')

	print "get_stream_query query_type "+ query_type
	if (query_type == 'artist' or query_type == 'label'):
		query = "("
	else:
		query = 'date:['+start_date +" TO "+ end_date+']'
		query += " AND "
		query += "("

	#if query_type == 'laid':
		# for mbid in mbids:
		# 	if mbids.index(mbid) == 0:
		# 		query = query + query_type+':' + mbid + ' '
		# 	else:
		# 		query = query + ' OR '+query_type+':' + mbid + ' '
	#else:
	for mbid in mbids:
		if mbids.index(mbid) == 0:
			query = query + query_type+': "' + mbid + '" '
		else:
			query = query + 'OR '+query_type+':"' + mbid + '" '

	query += ')'
	print query
	query = urllib.quote_plus(query.encode('utf8'))
	return query 

def get_album_tracks(request):
	# if request.user.is_authenticated():
	print "album_tracks was just called"
	get = request.GET.copy()
	print get
	reid = get[u"reid"]
	tracks = getTracklistByReid(reid)
	tracks = check_if_follows(request,'sounds', tracks)
	print "this is tracks on get album tracks"
	print tracks
	results = {'test':"is this working?", "reid":reid, 'tracks':tracks}
	return_json = simplejson.dumps(results)
	return HttpResponse(return_json, mimetype='application/json')
		#return HttpResponse("album page!!!")
	# else:
	# 	return HttpResponse('You must be logged in to do this', status=401)

def get_album_tracks_lastfm(request):
	# if request.user.is_authenticated():
	print "album_tracks lastfm was just called"
	get = request.GET.copy()
	print get
	# reid = get["reid"]
	artist = get["artist"]
	artist = urllib.quote_plus(artist)
	title = get["title"]
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
	tracks = check_if_follows(request,'sounds', tracks)
	print "this is tracks on get album tracks"
	print tracks
	results = {'tracks':tracks}
	#results = {"reid":reid, 'tracks':tracks}
	return_json = simplejson.dumps(results)
	return HttpResponse(return_json, mimetype='application/json')
		#return HttpResponse("album page!!!")
	# else:
	# 	return HttpResponse('You must be logged in to do this', status=401)


def artist_browse(request, artist_id):
	releases, rgids = get_browse_releases('artist', artist_id)
	releases = check_if_follows(request, 'labels', releases)
	releases = check_if_follows(request, 'artists', releases)
	return render_to_response('scrapers/home.html',{'page':'artist', 'releases':releases}, context_instance=RequestContext(request))
	#return HttpResponse("artist id: " +artist_id)




def label(request, label_id):
	releases, rgids = get_browse_releases('label', label_id)
	#return render_to_response('scrapers/home.html',{'page':'label', 'releases':releases})
	#return HttpResponse("label id: " +label_id)
	releases = check_if_follows(request, 'labels', releases)
	releases = check_if_follows(request, 'artists', releases)
	print "THIS IS LABEL releases: "
	print releases
	return render_to_response('scrapers/home.html',{'page':'label', 'releases':releases}, context_instance=RequestContext(request))




from registration.backends.simple.views import RegistrationView

class CustomRegistrationView(RegistrationView):
	# success_url = "/"
	# get_success_url(request, user)
	def get_success_url(self, request, user):
		return "/"


def lastfm_search(request):
	if request.GET:
		get = request.GET.copy()
		username = get['username']
		artists = get_lastfm_artists(username, 300)
		artists = check_if_follows(request, 'artists', artists)
		#return HttpResponse("Username found: %s" % username )
		return render_to_response('scrapers/home.html',{'page':'lastfm_search', 'artists':artists},context_instance=RequestContext(request))
		# call username API
		# send to template that charts out each 
	else:
		#return HttpResponse("No username")
		return render_to_response('scrapers/home.html', {'page':'lastfm_search'}, context_instance=RequestContext(request))


def soundcloud_search(request):
	get = request.GET.copy()
	username = get['username']
	query_type = get['query-type']
	print "GET REQUEST username: " + username
	print "get request type: " +query_type
	#query_type = get['query-type']
	limit = 200
	offset = 0
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

	results = []
	name_chunks = [names[x:x+100] for x in xrange(0, len(names), 100)]
	for names in name_chunks:
		query = get_stream_query(query_type, names)
		api_results = mbz_search(query, query_type)

		print "results search sees: "
		print api_results
		
		if query_type == 'label':
			# query_type = 'labels'
			for entry in api_results['labels']:
				print "api_results length: " + str(len(api_results))
				results.append({'name':entry['name'], 'label_id':entry['id']})
			
		elif query_type == 'artist':
			for entry in api_results['artist']:
				results.append({'name':entry['name'], 'artist_id':entry['id']})
			
	if query_type == 'label':
		results = check_if_follows(request, 'labels', results)
		return render_to_response('scrapers/home.html',{'page':'soundcloud', 'labels':results},context_instance=RequestContext(request))

	elif query_type == 'artist':
		results = check_if_follows(request, 'artists', results)
		return render_to_response('scrapers/home.html',{'page':'soundcloud', 'artists':results},context_instance=RequestContext(request))


def search(request):
	if request.GET:
		get = request.GET.copy()
		query = get['query']
		query = urllib.quote_plus(query.encode('utf8'))
		query_type = get['query-type']
		print "query: " +query
		#query_type = get['query-type']
		#query_type = 'artist'
		api_results = mbz_search(query, query_type)
		print "results search sees: "
		print api_results
		results = []

		if query_type == 'label':
			# query_type = 'labels'
			for entry in api_results['labels']:
				#print "api_results length: " + str(len(api_results))
				# print "ENTRY: "
				# print entry 
				results.append({'name':entry['name'], 'label_id':entry['id']})
				results = check_if_follows(request, 'labels', results)
			return render_to_response('scrapers/home.html',{'page':'search', 'labels':results},context_instance=RequestContext(request))
		if query_type == 'artist':
			for entry in api_results['artist']:
				results.append({'name':entry['name'], 'artist_id':entry['id']})
				results = check_if_follows(request, 'artists', results)
			return render_to_response('scrapers/home.html',{'page':'search', 'artists':results},context_instance=RequestContext(request))

	else:
		#return HttpResponse("No username")
		return render_to_response('scrapers/home.html', {'page':'search'}, context_instance=RequestContext(request))




def stream(request):
	if request.user.is_authenticated():
		artist_set = request.user.get_profile().artists.all()
		print artist_set
		artist_ids = []
		for artist in artist_set:
			artist_ids.append(artist.mbid)

		label_set = request.user.get_profile().labels.all()
		label_ids = []
		for label in label_set:
			label_ids.append(label.mbid)

		rgids = []
		releases = []

		#can be 103, not 100
		artist_id_chunks = [artist_ids[x:x+100] for x in xrange(0, len(artist_ids), 100)]
		for artist_ids in artist_id_chunks:
			query = get_stream_query('arid', artist_ids[0:100])
			new_releases, new_rgids = get_browse_releases('stream', query, rgids)
			releases +=new_releases
			rgids+= new_rgids


		label_id_chunks = [label_ids[x:x+100] for x in xrange(0, len(label_ids), 100)]
		for label_ids in label_id_chunks:
			query = get_stream_query('laid', label_ids)
			print query
			new_releases, new_rgids = get_browse_releases('stream', query, rgids)
			releases +=new_releases
			rgids+= new_rgids

		releases = check_if_follows(request, 'artists', releases)
		releases = check_if_follows(request, 'labels', releases)
		return render_to_response('scrapers/home.html',{'page':'stream', 'releases':releases}, context_instance=RequestContext(request))

	else:
		return HttpResponse("You need to be logged in to have a stream")


def check_if_follows(request, model_type, list_of_entities):
	if request.user.is_authenticated():
		print "check if follows, user is authenticated"
		#ARTISTS
		if model_type == 'artists':
	 		# model_entries = request.user.get_profile().artists.all()
	 		# mbids = []
		 	# for entry in model_entries:
		 	# 	mbids.append(entry.mbid)
		 	# for item in list_of_entities:
		 	# 	if item['artist_id'] in mbids:
		 	# 		item['following_artist'] = 'Following'
		 	# 		# item['following_artist'] = True
		 	# 	else:
		 	# 		item['following_artist'] = 'Follow'
		 	# 		# item['following_artist'] = False

		 	model_entries = request.user.get_profile().artists.all()
		 	for item in list_of_entities:
		 		try:
		 			artist = item['name']
		 		except KeyError:
		 			artist = item['artist']
		 		if model_entries.filter(name = artist).exists():

		 			item['following_artist'] = 'Following'
		 			# item['following_artist'] = True
		 		else:
		 			item['following_artist'] = 'Follow'
		 			# item['following_artist'] = False

		#LABELS
	 	if model_type == 'labels':
	 		model_entries = request.user.get_profile().labels.all()
		 	mbids = []
		 	for entry in model_entries:
		 		mbids.append(entry.mbid)
	 		for item in list_of_entities:
		 		if item['label_id'] in mbids:
		 			item['following_label'] = 'Following'
		 			# item['following_label'] = True
		 		else:
		 			item['following_label'] = 'Follow'
		 			# item['following_label'] = False
		#SOUNDS
		if model_type =='sounds':
			model_entries = request.user.get_profile().sounds.all()
		 	mbids = []
		 	for entry in model_entries:
		 		mbids.append(entry.mbid)
		 	for item in list_of_entities:
		 		if item['track_id'] in mbids:
		 			# item['following_sound'] = "You Like This"
		 			item['following_sound'] = True
		 			print "following sound"
		 		else:
		 			# item['following_sound'] = 'Like'
		 			item['following_sound'] = False
		 			print "not following sound"
		#ALBUMS
		if model_type =='albums':
			print "checking if following albums"
			model_entries = request.user.get_profile().albums.all()
			
		 	for item in list_of_entities:
		 		matches = model_entries.filter(artists__name__iexact =item['artist'], title__iexact = item['title'])
		 		if matches:
		 			item['following_album'] = True
		 			print "following album"
		 		else:
		 			item['following_album'] = False
		 			print "not following album"
		return list_of_entities

	else:
	 	for item in list_of_entities:
	 		item['following_artist'] = 'Follow'
	 		item['following_label'] = 'Follow'
	 		# item['following_sound'] = 'Like'
	 		item['following_sound'] = False

 		return list_of_entities


def my_follows(request):
	if request.user.is_authenticated():
		artist_set = request.user.get_profile().artists.all()
		artists = []
		for artist in artist_set:
			artists.append({'name':artist.name, 'artist_id':artist.mbid})
		artists = check_if_follows(request, 'artists', artists)

		album_set = request.user.get_profile().albums.all()
		albums = []
		for album in album_set:
			albums.append({'title': album.title, 'artist':album.artists.all()[0].name})
		albums = check_if_follows(request, 'albums', albums)


		label_set = request.user.get_profile().labels.all()
		labels = []
		for label in label_set:
			labels.append({'name':label.name, 'label_id':label.mbid})
		labels = check_if_follows(request, 'labels', labels)

		return render_to_response('scrapers/home.html',{'page':'my_follows', 'artists':artists, 'labels':labels, 'releases':albums}, context_instance=RequestContext(request))

	else:
		return HttpResponse("You need to be logged in to see followed artists and labels")

def my_sounds(request):
	if request.user.is_authenticated():
		sound_set = request.user.get_profile().sounds.all()
		sounds = []
		for sound in sound_set:
			sounds.append({'artist':sound.artists.all()[0], 'title':sound.title, 'mbid':sound.mbid})
			sounds = check_if_follows(request, 'sounds', sounds)
		# artists = check_if_follows(request, 'artists', artists)

		# label_set = request.user.get_profile().labels.all()
		# labels = []
		# for label in label_set:
		# 	labels.append({'name':label.name, 'label_id':label.mbid})
		# labels = check_if_follows(request, 'labels', labels)

		return render_to_response('scrapers/home.html',{'page':'my_sounds', 'sounds':sounds}, context_instance=RequestContext(request))

	else:
		return HttpResponse("You need to be logged in to see followed artists and labels")

def artist_by_name(request, artist):
	artist = urllib.quote(artist)
	url = "http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist="+artist+"&autocorrect=1&api_key="+lastfm_api_key+"&format=json"
	print "this is is the url artist_by_name sees " + url
	data = urllib2.urlopen(url)
	api_results = json.load(data)
	print api_results
	mbid = api_results['artist']['mbid']
	artist = api_results['artist']['name']
	# return_string = "Artist: %s mbid: %s" % (artist, mbid)
	# return HttpResponse(return_string)

	try:
		a = Artist.objects.get(name__iexact = artist)
		sound_set = a.sounds.all()
		sounds = []
		for sound in sound_set:
			sounds.append({'artist':sound.artists.all()[0], 'title':sound.title, 'mbid':sound.mbid})
	except:
		sounds = []


	releases, rgids = get_browse_releases('artist', mbid)
	releases = check_if_follows(request, 'labels', releases)
	releases = check_if_follows(request, 'artists', releases)
	releases = check_if_follows(request, 'albums', releases)
	return render_to_response('scrapers/home.html',{'page':'artist', 'releases':releases, 'sounds':sounds}, context_instance=RequestContext(request))


def all_sounds(request):
	sound_set = Sound.objects.all()
	sounds = []
	for sound in sound_set:
		if sound.yt_track_id:
			track = {"type":"yt", "id":sound.yt_track_id}
		elif sound.sc_track_id:
			track = {"type":"sc", "id":sound.sc_track_id}
		elif sound.vimeo_track_id:
			track = {"type":"vimeo", "id":sound.vimeo_track_id}
		else:
			track = {"type":"text"}

		if sound.artists.all():
			track['artist'] = sound.artists.all()[0]
			track['title'] = sound.title
			# sounds.append({' ':sound.artists.all()[0], 'title':sound.title})
			sounds.append(track)
			print sound.title
		else:
			track['title'] = sound.original_slug
			sounds.append(track)
			# sounds.append({'title':sound.original_slug})

	return render_to_response('scrapers/home.html',{'page':'my_sounds', 'sounds':sounds}, context_instance=RequestContext(request))


def songs_by_source(request, source_id):
	source = Source.objects.get(pk = source_id)
	title = source.url
	sound_set = source.sounds.all()
	sounds = []
	for sound in sound_set:
		if sound.yt_track_id:
			track = {"type":"yt", "id":sound.yt_track_id}
		elif sound.sc_track_id:
			track = {"type":"sc", "id":sound.sc_track_id}
		elif sound.vimeo_track_id:
			track = {"type":"vimeo", "id":sound.vimeo_track_id}
		else:
			track = {"type":"text"}

		if sound.artists.all():
			track['artist'] = sound.artists.all()[0]
			track['title'] = sound.title
			# sounds.append({' ':sound.artists.all()[0], 'title':sound.title})
			sounds.append(track)
			print sound.title
		else:
			track['title'] = sound.original_slug
			sounds.append(track)
			# sounds.append({'title':sound.original_slug})

	return render_to_response('scrapers/home.html',{'page':'my_sounds', 'title': title, 'sounds':sounds}, context_instance=RequestContext(request))

# def full_search(request):
# 	if request.GET:
# 		get = request.GET.copy()
# 		query = get['query']
# 		query = urllib.quote_plus(query.encode('utf8'))
# 		# query_type = get['query-type']
# 		print "query: " +query

# 		album_url = "http://ws.audioscrobbler.com/2.0/?method=album.search&album="+query+"&api_key=c43db4e93f7608bb10d96fa5f69a74a1&format=json"
# 		data = urllib2.urlopen(album_url)
# 		album_results = json.load(data)
# 		print album_url
# 		releases = []
# 		if album_results['results']['albummatches'] is not " ":
# 			for album in album_results['results']['albummatches']['album']:
# 				artist = album['artist']
# 				title = album['name']
# 				releases.append({'artist':artist,'title':title})
			

# 		artist_url = "http://ws.audioscrobbler.com/2.0/?method=artist.search&artist="+query+"&api_key=c43db4e93f7608bb10d96fa5f69a74a1&format=json"
# 		print artist_url
# 		data = urllib2.urlopen(artist_url)
# 		artist_results = json.load(data)
# 		artists = []
# 		for artist in artist_results['results']['artistmatches']['artist']:
# 			artist_name = artist['name']
# 			artists.append({'artist':artist_name})



# 		track_url = "http://ws.audioscrobbler.com/2.0/?method=track.search&track="+query+"&api_key=c43db4e93f7608bb10d96fa5f69a74a1&format=json"
# 		data = urllib2.urlopen(album_url)
# 		track_results = json.load(data)
# 		tracks = []
# 		for track in track_results['results']['trackmatches']['track']:
# 			artist = track['artist']
# 			title = track['title']
# 			tracks.append({"artist":artist, 'title':title})



# 		#query_type = get['query-type']
# 		#query_type = 'artist'
# 		api_results = mbz_search(query, query_type)
# 		print "results search sees: "
# 		print api_results
# 		results = []

# 		if query_type == 'label':
# 			# query_type = 'labels'
# 			for entry in api_results['labels']:
# 				#print "api_results length: " + str(len(api_results))
# 				# print "ENTRY: "
# 				# print entry 
# 				results.append({'name':entry['name'], 'label_id':entry['id']})
# 				results = check_if_follows(request, 'labels', results)
# 			return render_to_response('scrapers/home.html',{'page':'search', 'labels':results},context_instance=RequestContext(request))
# 		if query_type == 'artist':
# 			for entry in api_results['artist']:
# 				results.append({'name':entry['name'], 'artist_id':entry['id']})
# 				results = check_if_follows(request, 'artists', results)
# 			return render_to_response('scrapers/home.html',{'page':'search', 'artists':results},context_instance=RequestContext(request))

# 	else:
# 		#return HttpResponse("No username")
# 		return render_to_response('scrapers/home.html', {'page':'search'}, context_instance=RequestContext(request))

def full_search(request):
	if request.GET:
		get = request.GET.copy()
		query = get['query']
		query = urllib.quote_plus(query.encode('utf8'))
		# query_type = get['query-type']
		print "query: " +query
		#query_type = get['query-type']
		#query_type = 'artist'
		
		#LABEL
		api_results = mbz_search(query, 'label', limit=10)
		print "results search sees: "
		print api_results
		labels = []
		mbids = []
		for entry in api_results['labels']:
			if len(labels) < 5:
				if entry["id"] not in mbids:
					mbids.append(entry["id"])
					#print "api_results length: " + str(len(api_results))
					# print "ENTRY: "
					# print entry 
					labels.append({'name':entry['name'], 'label_id':entry['id']})
					labels = check_if_follows(request, 'labels', labels)


		# ARTIST		
		artist_url = "http://developer.echonest.com/api/v4/artist/extract?api_key=FBHCMLQRHBCWD8GVA&format=json&text="+query+"&results=10"
		data = urllib2.urlopen(artist_url)
		artist_results = json.load(data)
		print artist_url
		artists = []
		for entry in artist_results['response']['artists']:
			if len(artists) < 5:
				artists.append({'name':entry['name']})
				artists = check_if_follows(request, 'artists', artists)


		if not artists:
			api_results = mbz_search(query, 'artist', limit=10)
			print "results search sees: "
			print api_results
			artists = []
		# while len(artists) < 5:
			for entry in api_results['artist']:
				if len(artists) < 5:
					if entry["id"] not in mbids:
						mbids.append(entry["id"])
						artists.append({'name':entry['name'], 'artist_id':entry['id']})
						# artists = check_if_follows(request, 'artists', artists)


	# 	#search releases
	# 	api_results = mbz_search(query, 'release-group', limit=10)
	# 	print "results search sees: "
	# 	print api_results
	# 	releases = []
	# # while len(artists) < 5:
	# 	for entry in api_results['release-groups']:
	# 		if len(releases) < 5:
	# 			if entry["id"] not in mbids:
	# 				mbids.append(entry["id"])
	# 				releases.append({'title':entry['title'], 'artist':entry['artist-credit'][0]['artist']['name']})
	# 				# releases = check_if_follows(request, 'artists', artists)
	# 	print releases

		#search releases
		api_results = mbz_search(query, 'release', limit=10)
		print "results search sees: "
		print api_results
		rgids = []
		parsed_results = parse_releases(api_results, rgids)
		releases = parsed_results['releases']
		rgids = parsed_results['rgids']
		releases = check_if_follows(request, 'labels', releases)
		releases = check_if_follows(request, 'artists', releases)
		releases = check_if_follows(request, 'albums', releases)
		print releases




	# 	api_results = mbz_search(query, 'recording', limit=10)
	# 	print "results search sees: "
	# 	print api_results
	# 	recordings = []
	# # while len(artists) < 5:
	# 	for entry in api_results['recording']:
	# 		if len(recordings) < 5:
	# 			if entry["id"] not in mbids:
	# 				mbids.append(entry["id"])
	# 				recordings.append({'title':entry['title'], 'artist':entry['artist-credit'][0]['artist']['name']})
	# 				# releases = check_if_follows(request, 'artists', artists)
	# 	print recordings

		track_url = "http://ws.audioscrobbler.com/2.0/?method=track.search&track="+query+"&api_key=c43db4e93f7608bb10d96fa5f69a74a1&format=json"
		data = urllib2.urlopen(track_url)
		track_results = json.load(data)
		tracks = []
		for track in track_results['results']['trackmatches']['track']:
			artist = track['artist']
			title = track['name']
			tracks.append({"artist":artist, 'title':title, 'type':'text'})
		recordings = tracks

		return render_to_response('scrapers/home.html',{'page':'search', 'artists':artists, 'labels':labels, 'releases':releases, 'sounds':recordings},context_instance=RequestContext(request))
	
	else:
		return render_to_response('scrapers/home.html', {'page':'search'}, context_instance=RequestContext(request))


def import_artists(request):
	return render_to_response('scrapers/home.html',{'page':'advanced_search'},context_instance=RequestContext(request))


def playlist_view(request, playlist_id):
	playlist = User_playlist.objects.get(pk =playlist_id)


	tracks = []
	albums = []
	for pl_entry in playlist.entries.all():

		if pl_entry.sound:
			entry = pl_entry.sound
			track = {'title':entry.title, 'type': 'text'}
			if entry.mbid:
				track_id = entry.mbid
				artist_name = entry.artists.all()[0].name
				artist_id = entry.artists.all()[0].mbid 
				track.update({'track_id':track_id, 'artist':artist_name, 'artist_id':artist_id})
				print "this is the playlistview processed track" 
				print track
			elif entry.artist_name:
				artist_name = entry.artist_name
				track.update({"artist":artist_name})
			tracks.append(track)

		if pl_entry.album:
			entry = pl_entry.album
			album = {'title': entry.title}
			if entry.reid:
				release_id = entry.reid
				artist_name = entry.artists.all()[0].name
				artist_id = entry.artists.all()[0].mbid
				album['reid'] = release_id
				album['artist'] = artist_name
				album['artist_id'] = artist_id

			elif track['artist_name']:
				artist_name = entry.artist_name
				album['artist_name'] = artist_name
			albums.append(album)

	if albums or tracks:
		return render_to_response('scrapers/home.html',{'page':'search', 'releases':albums, 'sounds':tracks},context_instance=RequestContext(request))
	else:
		return HttpResponse("This is an empty playlist, add search to add albums and songs! Playlist #"+str(playlist_id))


from django.shortcuts import render
from django.http import HttpResponseRedirect

def create_playlist(request):
	if request.user.is_authenticated():
		if request.method == 'POST': # If the form has been submitted...
			form = PlaylistForm(request.POST) # A form bound to the POST data
			if form.is_valid():
				playlist = form.save()
				pk = playlist.pk
				user = request.user
				print user
				user_profile, up_created = UserProfile.objects.get_or_create(user = user)
				print "user profile created: " + str(up_created)
				print user_profile.user.username
				playlist.users.add(user_profile)
				playlist.save()

		     # All validation rules pass
		        # Process the data in form.cleaned_data
		        # ...
		        return HttpResponseRedirect('/playlist/'+str(pk)) # Redirect after POST
		else:
			form = PlaylistForm() # An unbound form

		return render_to_response('scrapers/home.html', {'page':"create_playlist", 'form': form}, context_instance=RequestContext(request))
	else:
		return HttpResponse("You need to be logged in to make playlists")

from django.forms import ModelForm
class PlaylistForm(ModelForm):
    class Meta:
        model = User_playlist
        fields = ('name', 'description')


def get_playlists(request):
	if request.user.is_authenticated():
		user = request.user
		# user_profile, up_created = UserProfile.objects.get_or_create(user = user)
		# playlist_set = user_profile.user_playlists.all()
		# playlists = []
		# for entry in playlist_set:
		# 	playlist = {"name":entry.name, "pk":entry.pk,'description':entry.description}
		# 	playlists.append(playlist)
		playlists = get_user_playlists(user)		
		results = {'playlists':playlists}

		return_json = simplejson.dumps(results)
		return HttpResponse(return_json, mimetype='application/json')
	else:
		return HttpResponse("You need to be logged in to make playlists", status=401)


def get_user_playlists(user):
	user_profile, up_created = UserProfile.objects.get_or_create(user = user)
	playlist_set = user_profile.user_playlists.all()
	playlists = []
	for entry in playlist_set:
		playlist = {"name":entry.name, "pk":entry.pk,'description':entry.description}
		playlists.append(playlist)
	return playlists





def add_album_to_playlist(request):
	if request.user.is_authenticated():
		user = request.user
		user_profile, up_created = UserProfile.objects.get_or_create(user = user)
		if request.method == 'POST':
			post = request.POST.copy()
			title = post['title']
			reid = post['reid']
			artist_name = post['artist_name']
			release = get_or_create_release(title = title, artist_name = artist_name, reid = reid)
			playlist_id = post['playlist_id']
			playlist = User_playlist.objects.get(pk =playlist_id)

			playlist_entry = User_playlist_entry(album = release, user_playlist = playlist)
			playlist_entry.save()

		return HttpResponse('success')
	else:
		return HttpResponse("You need to be logged in to make playlists",  status=401)

def add_track_to_playlist(request):
	if request.user.is_authenticated():
		user = request.user
		user_profile, up_created = UserProfile.objects.get_or_create(user = user)
		if request.method == 'POST':
			post = request.POST.copy()
			title = post['title']
			mbid = post['mbid']
			artist_name = post['artist_name']
			sound = get_or_create_recording(title = title, artist_name = artist_name, mbid = mbid)
			playlist_id = post['playlist_id']
			playlist = User_playlist.objects.get(pk =playlist_id)

			playlist_entry = User_playlist_entry(sound = sound, user_playlist = playlist)
			playlist_entry.save()

		return HttpResponse('success')
	else:
		return HttpResponse("You need to be logged in to make playlists",  status=401)


def my_playlists(request):
	if request.user.is_authenticated():
		user = request.user
		playlists = get_user_playlists(user)	

		return render_to_response('scrapers/home.html', {'page':"my_playlist", 'playlists':playlists}, context_instance=RequestContext(request))
	else:
		return HttpResponse("You need to be logged in to have playlists")










