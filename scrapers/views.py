# Create your views here.
# Create your views here.


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


#@login_required(login_url='/accounts/login/')
def get_album_tracks(request):
	# if request.user.is_authenticated():
	print "album_tracks was just called"
	get = request.GET.copy()
	print get
	reid = get[u"reid"]
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
	# results = {'reid':reid, 'tracks':tracks}
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
	reid = get["reid"]
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

def mbz_search(query, query_type, limit =100):
	url = "http://musicbrainz.org/ws/2/"+query_type+"/?query="+query+"&fmt=json&limit="+str(limit)
	print "QUERY URL: " + url
	data = urllib2.urlopen(url)
	api_results = json.load(data)
	#print api_results
	return api_results




# def get_artist_by_mbid(artist_id, artist_name):
# 	artist, artist_created = Artist.objects.get_or_create(mbid = artist_id)
# 	print artist 
# 	if artist_created:
# 		# artist.name = get_english_alias('artist', artist_id)
# 		artist.name = artist_name
# 		artist.save()
# 		print "added artist"
# 	return artist

# def get_label_by_mbid(label_id, label_name):
# 	label, label_created = Label.objects.get_or_create(mbid = label_id)
# 	print label 
# 	if label_created:
# 		# label.name = get_english_alias('label', label_id)
# 		label.name = label_name
# 		label.save()
# 		print "added label"
# 	return label

# def get_album_by_reid(artist_id, artist_name, title, reid):

# 	album, album_created = Album.objects.get_or_create(mbid = reid)
# 	print album
	
	
# 	if album_created:
# 		artist = get_artist_by_mbid(artist_id, artist_name)
# 		album.title = title
# 		album.artists.add(artist)
# 		# album.name = get_english_alias('label', label_id)
# 		album.save()
# 		print "added album"
# 	return album

# def get_sound_by_mbid(sound_id, artist_id, artist_name, title):
# 	sound, sound_created = Sound.objects.get_or_create(mbid = sound_id)
# 	print sound

# 	if sound_created:
# 		artist = get_artist_by_mbid(artist_id, artist_name)
# 		sound.title = title
# 		sound.artists.add(artist)
# 		sound.save()
# 		print "sound added"
# 	return sound



# def get_sound_without_mbid(artist_name, title):
# 	sound, sound_created = Sound.objects.get_or_create(title = title, artist_name = artist_name)
# 	return sound

# def get_album_without_mbid(artist_name, title):
# 	album, album_created = Album.objects.get_or_create(title =title, artist_name = artist_name)
# 	return album 





def follow_toggle(request):
	if request.user.is_authenticated():
		user = request.user
		user_profile, up_created = UserProfile.objects.get_or_create(user = user)

		post = request.POST.copy()

		if post['type'] == 'artist':
			print "type: artist "
			artist_name = post['artist_name']
			# print artist_name 
			artist_id = post['artist_id']
			# artist, artist_created = Artist.objects.get_or_create(name = artist_name)
			artist = get_artist_by_mbid(artist_id, artist_name)

			if artist in user_profile.artists.all():
			# if user_profile.artists.filter(name = artist_name).exists():
				user_profile.artists.remove(artist)
				user_profile.save()
				print "unfollowed artist"

			else:
				user_profile.artists.add(artist)
				user_profile.save()
				print "followed artist"


		elif post['type'] == 'label':
			print "type: label "
			label_id = post['label_id']
			lable_name = post['label_name']
			print label_id

			label = get_label_by_mbid(label_id, label_name)

			if label in user_profile.labels.all():
			# if user_profile.labels.filter(mbid = label_id).exists():
				user_profile.labels.remove(label)
				user_profile.save()
				print "unfollowed label"

			else:
				user_profile.labels.add(label)
				user_profile.save()
				print "followed label"

		# try:
		elif post['type'] == 'track':
			pass
			print "type: track "
			track_id = post['track_id']
			print track_id
			sound, sound_created = Sound.objects.get_or_create(mbid = track_id)
			print sound 
			if sound_created:
				url = "http://www.musicbrainz.org/ws/2/recording/"+track_id+"?fmt=json&inc=artist-credits"
				data = urllib2.urlopen(url)
				api_results = json.load(data)
				sound.title = api_results['title']
				sound.save()
				print "added sound"

				for artist in api_results['artist-credit']:
					artist_id = artist['artist']['id']
					artist = get_artist_by_mbid(artist_id)
					sound.artists.add(artist)
					sound.save()

			if user_profile.sounds.filter(mbid = track_id).exists():
				user_profile.sounds.remove(sound)
				user_profile.save()
				print "unfollowed sound"

			else:
				user_profile.sounds.add(sound)
				user_profile.save()
				print "followed sound"

		# if post['type'] == 'release':
		# 	print "type: release "
		# 	try:
		# 		reid = post['reid']
		# 	except:
		# 		reid = ""

		# 	artist = post['artist']
		# 	title = post['title']

		# 	artist, artist_created = Artist.objects.get_or_create(name = artist)

		# 	if not artist_created:
		# 		albums = artist.albums.all()
		# 		albums = albums.get(title = title)
		# 		if albums:
		# 			album = albums[0]
		# 		else:
		# 			album = Album.objects.create(title = title)
		# 			album.artists.add(artist)
		# 			album.save()

		# 		user_profile.add(album)
		# 		user_profile.save()

		# 	else:
		# 		album = Album.create(title = title)
		# 		album.artists.add(artist)
		# 		album.save()
		# 		user_profile.add(album)
		# 		user_profile.save()

		# 	album = Album.objects.get_or_create(title = title)
		# 	if album[1]:

		# 	# album = Album.create(title = title)
		# 		album.artists.add(artist)
		# 		if reid:
		# 			album.album_type = "release"
		# 			album.mbid = reid
		# 		else:
		# 			album.album_type = "scraped"

		# 		album.save()



		#release
		# if post['type'] == 'release':
		# 	print "type: release "
		# 	reid = post['reid']
		# 	print reid
		# 	release, release_created = Release.objects.get_or_create(release_id = reid)
		# 	print release 
		# 	if release_created:
		# 		url = "http://www.musicbrainz.org/ws/2/release/"+reid+"?fmt=json&inc=labels+release-groups+recordings+artist-credits"
		# 		print "This is the release url " + url
		# 		data = urllib2.urlopen(url)
		# 		api_results = json.load(data)
		# 		release.title = api_results['title']
		# 		release.save()
		# 		print "added release"

		# 		release.date_released_string = api_results['date']
		# 		release.primary_type = api_results['release-group']['primary_type']
		# 		release.secondary_types = "".join(api_results['release-group']['secondary_types'])

		# 		for label in api_results['label-info']:
		# 			try:
		# 				label_id = label['id']
		# 				label_name = label['name']
		# 				label, label_created = Label.objects.get_or_create(mbid = label_id)
		# 				label.save()
		# 				if label_created:
		# 					label.name = label_name
		# 					label.save()
		# 				release.labels.add(label)
		# 				release.save()
		# 			except:
		# 				print "no label info"
		# 			try:
		# 				release.catalog_number = label["catalog-number"]
		# 				release.save()
		# 			except:
		# 				print "no catalog number"


		# 		for artist in api_results['artist-credit']:
		# 			artist_id = artist['artist']['id']
		# 			artist = get_artist_by_mbid(artist_id)
		# 			release.artists.add(artist)
		# 			release.save()

		# 	if user_profile.releases.filter(release_id = reid).exists():
		# 		user_profile.releases.remove(releases)
		# 		user_profile.save()
		# 		print "unfollowed release"

		# 	else:
		# 		user_profile.releases.add(release)
		# 		user_profile.save()
		# 		print "followed release"


		return HttpResponse("you're logged in!! " + request.user.username)
	else:
		return HttpResponse('You must be logged in to do this', status=401)


def follow_album(request):
	if request.user.is_authenticated():
		user = request.user
		user_profile, up_created = UserProfile.objects.get_or_create(user = user)

		post = request.POST.copy()
		post_type = post['type']
		print post_type
		if post_type == 'album':
			print "type: album "
			# artist_name = post['artist_name']
			# print artist_name 
			artist_name = post['artist']
			title = post['title']
			reid = post['reid']

			album = get_or_create_album_by_artist_and_title(artist_name, title, reid)
			# artist = get_artist_by_mbid(artist_id)


			if album in user_profile.albums.all():
				user_profile.albums.remove(album)
				user_profile.save()
				print "unfollowed album"

			else:
				user_profile.albums.add(album)
				user_profile.save()
				print "followed album"

		return HttpResponse("you're logged in!! " + request.user.username)
	else:
		return HttpResponse('You must be logged in to do this', status=401)


# def get_or_create_album_by_artist_and_title(artist, title):
# 	url = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=c43db4e93f7608bb10d96fa5f69a74a1&artist="+artist+"&album="+title+"&autocorrect=1&format=json"
# 	data = urllib2.urlopen(url)
# 	results = json.load(data)
# 	try:
# 		mbid = results['album']['mbid']
# 	except:
# 		mbid = ""
# 	artist = results['album']['artist']
# 	title = results['album']['name']

# 	artist, artist_created = Artist.objects.get_or_create(name = artist)

# 	album, album_created = Album.objects.get_or_create(mbid = mbid)

# 	if album_created:
# 		album.title = title
# 		album.album_type = "reid"
# 		album.artists.add(artist)
# 		album.save()

# 	return album 



def get_or_create_album_by_artist_and_title(artist, title, reid=""):
	artist, artist_created = Artist.objects.get_or_create(name = artist)
	artist_albums = artist.albums.all()
	filtered_albums = artist_albums.filter(title = title)
	if not filtered_albums:
		album = Album.objects.create(title = title)
		album.artists.add(artist)
		album.save()
	else:
		album = filtered_albums[0]
	return album 





# def get_or_create_album_by_reid(reid):
# 	album, album_created = Album.objects.get_or_create(mbid = reid)
# 	if album_created:

# 		album = 

	
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

