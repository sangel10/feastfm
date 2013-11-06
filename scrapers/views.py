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
from scrapers.external_APIs import *
from scrapers.db_handler import *


mbz.set_useragent("feast", "0.0.0", "santiagoangel10@gmail.com")

sc_client_id = 'a0b4638bae6d50a9296f7fc3f35442eb'
lastfm_api_key = "c43db4e93f7608bb10d96fa5f69a74a1"




from registration.backends.simple.views import RegistrationView

class CustomRegistrationView(RegistrationView):
	# success_url = "/"
	# get_success_url(request, user)
	def get_success_url(self, request, user):
		return "/"


# @login_required(login_url='/accounts/login/')
def home(request):
	# return render_to_response('scrapers/home_search.html', context_instance = RequestContext(request))
	return render_to_response('scrapers/home_search.html', {'page':'home_search'}, context_instance=RequestContext(request))



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
	try:
		print query
	except Exception as e:
		print e
	query = urllib.quote_plus(query.encode('utf8'))
	return query 

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
		return render_to_response('scrapers/message.html', {'message':'no username was provided'}, context_instance=RequestContext(request))



def soundcloud_search(request):
	get = request.GET.copy()
	username = get['username']
	query_type = get['query-type']
	print "GET REQUEST username: " + username
	print "get request type: " +query_type
	#query_type = get['query-type']
	limit = 200
	offset = 0
	names = getSoundcloudUserFollow(username, limit, offset)


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
				# print "api_results length: " + str(len(api_results))
				results.append({'name':entry['name'], 'label_id':entry['id']})
		# if query_type == 'label':
			results = check_if_follows(request, 'labels', results)
			return render_to_response('scrapers/home.html',{'page':'soundcloud', 'labels':results},context_instance=RequestContext(request))


			
		elif query_type == 'artist':
			for entry in api_results['artist']:
				results.append({'name':entry['name'], 'artist_id':entry['id']})
		# elif query_type == 'artist':
			results = check_if_follows(request, 'artists', results)
			return render_to_response('scrapers/home.html',{'page':'soundcloud', 'artists':results},context_instance=RequestContext(request))


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
		# return HttpResponse("You need to be logged in to have a stream")
		message = "You need to be logged in to have a stream"
		return render_to_response('scrapers/message.html', {'message': message }, context_instance=RequestContext(request))



def my_follows(request):
	if request.user.is_authenticated():
		artist_set = request.user.get_profile().artists.all()
		artists = []
		for artist in artist_set:
			artists.append({'name':artist.name, 'artist_id':artist.mbid})
		artists = check_if_follows(request, 'artists', artists)


		label_set = request.user.get_profile().labels.all()
		labels = []
		for label in label_set:
			labels.append({'name':label.name, 'label_id':label.mbid})
		labels = check_if_follows(request, 'labels', labels)

		if artists or labels:
			return render_to_response('scrapers/home.html',{'page':'my_follows', 'artists':artists, 'labels':labels, }, context_instance=RequestContext(request))
		else:
			return render_to_response('scrapers/message.html', {'message': "You haven't followed anyone yet" }, context_instance=RequestContext(request))

	else:
		# return HttpResponse("You need to be logged in to see followed artists and labels")
		return render_to_response('scrapers/message.html', {'message': "You need to be logged in to see followed artists and labels" }, context_instance=RequestContext(request))

def my_sounds(request):
	if request.user.is_authenticated():
		sound_set = request.user.get_profile().sounds.all()
		sounds = []
		for sound in sound_set:
			if sound.artists.all():
				artist = sound.artists.all()[0].name
				artist_id = sound.artists.all()[0].mbid
			elif sound.artist_name:
				artist = sound.artist_name
				artist_id = ""
			else:
				artist = ""
				artist_id = ""
			sounds.append({'artist':artist, 'artist_id':artist_id, 'title':sound.title, 'mbid':sound.mbid})
		sounds = check_if_follows(request, 'sounds', sounds)


		album_set = request.user.get_profile().albums.all()
		albums = []
		for album in album_set:
			if album.artists.all():
				artist = album.artists.all()[0].name
				artist_id = album.artists.all()[0].mbid
			elif album.artist_name:
				artist = album.artist_name
				artist_id = ""
			else:
				artist = ""
				artist_id = ""
			albums.append({'title': album.title, 'artist':artist, 'artist_id':artist_id,})
		albums = check_if_follows(request, 'albums', albums)
		albums = check_if_follows(request, 'artists', albums)
		print "these are the my_follows albums: "
		print albums

		if sounds or albums:
			return render_to_response('scrapers/home.html',{'page':'my_sounds', 'sounds':sounds, 'releases':albums}, context_instance=RequestContext(request))
		else:
			return render_to_response('scrapers/message.html', {'message': "You haven't saved any songs or releases yet" }, context_instance=RequestContext(request))
		
	else:
		# return HttpResponse("You need to be logged in to see followed artists and labels")
		return render_to_response('scrapers/message.html', {'message': "You need to be logged in to your saved sounds" }, context_instance=RequestContext(request))


#depreciated
def artist_by_name(request, artist):
	artist = urllib.quote(artist)
	url = "http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist="+artist+"&autocorrect=1&api_key="+lastfm_api_key+"&format=json"
	print "this is is the url artist_by_name sees " + url
	data = urllib2.urlopen(url)
	api_results = json.load(data)
	print api_results
	mbid = api_results['artist']['mbid']
	artist = api_results['artist']['name']

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


def searchArtists(request, query, limit =5):
	artists = []
	api_results = mbz_search(query, 'artist', limit=limit)
	print "results search sees: "
	print api_results
	artists = []
	for entry in api_results['artist']:
		if len(artists) < limit:
			# if entry["id"] not in mbids:
			# 	mbids.append(entry["id"])
			if "disambiguation" in entry:
				disambiguation = entry['disambiguation']
			else:
				disambiguation = ""
			artists.append({'name':entry['name'], 'artist_id':entry['id'], 'disambiguation':disambiguation})
			artists = check_if_follows(request, 'artists', artists)
	return artists

def searchLabels(request, query, limit = 5):
	api_results = mbz_search(query, 'label', limit=limit)
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
				if 'disambiguation' in entry:
					disambiguation = entry['disambiguation']
				else:
					disambiguation = ""
				labels.append({'name':entry['name'], 'label_id':entry['id'], 'disambiguation':disambiguation})
				labels = check_if_follows(request, 'labels', labels)
	return labels

def searchReleases(request, query, limit=10):
	api_results = mbz_search(query, 'release', limit=limit)
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
	return releases

def searchLastfmTracks(request, query):
	try:
		track_url = "http://ws.audioscrobbler.com/2.0/?method=track.search&track="+query+"&api_key=c43db4e93f7608bb10d96fa5f69a74a1&format=json"
		data = urllib2.urlopen(track_url)
		track_results = json.load(data)

		tracks = []
		for track in track_results['results']['trackmatches']['track']:
			artist = track['artist']
			title = track['name']
			tracks.append({"artist":artist, 'title':title, 'type':'text'})
		recordings = tracks
	except:
		recordings = []
	recordings = check_if_follows(request, 'sounds', recordings)
	return recordings


def full_search(request):
	if request.GET:
		get = request.GET.copy()
		query = get['query']
		query = urllib.quote_plus(query.encode('utf8'))
		print "query: " +query

		labels = searchLabels(request, query)
		artists = searchArtists(request, query)
		releases = searchReleases(request, query)
		recordings = searchLastfmTracks(request, query)


		return render_to_response('scrapers/home.html',{'page':'search', 'artists':artists, 'labels':labels, 'releases':releases, 'sounds':recordings},context_instance=RequestContext(request))
	
	else:
		return render_to_response('scrapers/home.html', {'page':'search'}, context_instance=RequestContext(request))


def artist_search_view(request):
	if 'query' in request.GET:
		get = request.GET.copy()
		query = get['query']
		query = urllib.quote_plus(query.encode('utf8'))
		artists = searchArtists(request, query)
		return render_to_response('scrapers/home.html',{'page':'artist_search', 'artists':artists},context_instance=RequestContext(request))
	else:
		return render_to_response('scrapers/home.html', {'page':'search'}, context_instance=RequestContext(request))


def playlist_view(request, playlist_id):
	playlist = User_playlist.objects.get(pk =playlist_id)

	tracks = []
	albums = []
	for pl_entry in playlist.entries.all():

		if pl_entry.sound:
			entry = pl_entry.sound
			entry_id = pl_entry.pk
			track = {'title':entry.title, 'type': 'text', 'entry_id':entry_id}
			if entry.mbid:
				track_id = entry.mbid
				feast_id = entry.pk
				artist_name = entry.artists.all()[0].name
				artist_id = entry.artists.all()[0].mbid 
				track.update({'track_id':track_id, 'artist':artist_name, 'artist_id':artist_id, 'feast_id':feast_id})
				print "this is the playlistview processed track" 
				print track
			elif entry.artist_name:
				artist_name = entry.artist_name
				track.update({"artist":artist_name})
			tracks.append(track)

		if pl_entry.album:
			entry = pl_entry.album
			entry_id = pl_entry.pk
			album = {'title': entry.title, 'entry_id':entry_id}
			if entry.reid:
				release_id = entry.reid
				feast_id = entry.pk
				artist_name = entry.artists.all()[0].name
				artist_id = entry.artists.all()[0].mbid
				album['reid'] = release_id
				album['artist'] = artist_name
				album['artist_id'] = artist_id
				album['feast_id'] = feast_id


			elif track['artist_name']:
				artist_name = entry.artist_name
				album['artist_name'] = artist_name
			albums.append(album)
		this_playlist = {"name":playlist.name,'description':playlist.description, 'pk':playlist.pk}
	if albums or tracks:
		return render_to_response('scrapers/home.html',{'page':'playlist', 'releases':albums, 'sounds':tracks, 'playlist':this_playlist},context_instance=RequestContext(request))
	else:
		message = "This is an empty playlist, search to add albums and songs!"
		return render_to_response('scrapers/message.html', {'message':message }, context_instance=RequestContext(request))

from django.shortcuts import render
from django.http import HttpResponseRedirect

def create_playlist(request):
	if request.user.is_authenticated():
		if request.method == 'POST': 
			form = PlaylistForm(request.POST) 
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


		        return HttpResponseRedirect('/playlist/'+str(pk)) 
		else:
			form = PlaylistForm()

		# return render_to_response('scrapers/home.html', {'page':"create_playlist", 'form': form}, context_instance=RequestContext(request))
		return render_to_response('scrapers/create_playlist.html', {'page':"create_playlist", 'form': form}, context_instance=RequestContext(request))
	else:
		# return HttpResponse("You need to be logged in to make playlists")
		message = "You need to be logged in to make playlists"
		return render_to_response('scrapers/message.html', {'message':message }, context_instance=RequestContext(request))




from django.forms import ModelForm
class PlaylistForm(ModelForm):
    class Meta:
        model = User_playlist
        fields = ('name', 'description')



def my_playlists(request):
	if request.user.is_authenticated():
		user = request.user
		playlists = get_user_playlists(user)	
		# return render_to_response('scrapers/home.html', {'page':"my_playlist", 'playlists':playlists}, context_instance=RequestContext(request))
		return render_to_response('scrapers/my_playlists.html', {'page':"my_playlist", 'playlists':playlists}, context_instance=RequestContext(request))
	else:
		# return HttpResponse("You need to be logged in to have playlists")
		return render_to_response('scrapers/message.html', {'message': "You need to be logged in to have playlists" }, context_instance=RequestContext(request))





