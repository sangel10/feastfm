
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from scrapers.models import *
from scrapers.mbz_module import *


# from external_APIs import *
import simplejson


# import musicbrainzngs as mbz
# mbz.set_useragent("feast", "0.0.0", "santiagoangel10@gmail.com")





def get_or_create_artist_by_mbid(mbid):
	artist, artist_created = Artist.objects.get_or_create(mbid = mbid)
	if artist_created:
		artist_data = getArtistByID(mbid)
		artist.name = artist_data['name']
		artist.save()
	return artist

def get_or_create_label_by_mbid(mbid):
	label, label_created = Label.objects.get_or_create(mbid = mbid)
	if label_created:
		label_data = getLabelByID(mbid)
		label.name = label_data['name']
		label.save()
	return label


def get_or_create_recording_by_mbid(mbid):
	recording, recording_created = Sound.objects.get_or_create(mbid=mbid)
	if recording_created:
		recording_data = getRecordingByID(mbid)
		for entry in recording_data['artists']:
			artist, artist_created = Artist.objects.get_or_create(name=entry['artist_name'], mbid= entry['artist_id'])
			recording.artists.add(artist)
		recording.title = recording_data['title']
		recording.save()
	return recording

def get_or_create_release_by_mbid(reid):
	release, release_created = Album.objects.get_or_create(reid=reid)
	if release_created:
		release_data = getReleaseByID(reid)
		print "getReleaseByID results" 
		print release_data
		for entry in release_data['artists']:
			artist, artist_created = Artist.objects.get_or_create(name=entry['artist_name'], mbid= entry['artist_id'])
			release.artists.add(artist)
		release.title = release_data['title']
		release.save()
	else:
		print "Release already exists"
	return release 


#creates recording with or without MBID
def get_or_create_recording(title = '', artist_name = '', mbid =''):
	if mbid:
		recording = get_or_create_recording_by_mbid(mbid)
		return recording
	elif title and artist_name:
		recording, created = Sound.objects.get_or_create(title = title, artist_name = artist_name)
		return recording
	else:
		print "Error, get_or_create_release requires either an MBID or a title and an artist_name"


#creates release with or without mbid
def get_or_create_release(title = '', artist_name = '', reid=''):
	if reid:
		release = get_or_create_release_by_mbid(reid)
		print "get or create release by mbid"
		return release
	elif title and artist_name:
		release, created = Album.objects.get_or_create(title = title, artist_name = artist_name)
		return release
	else:
		print "Error, get_or_create_release requires either an MBID or a title and an artist_name"
	


def follow_toggle(request):
	if request.user.is_authenticated():
		user = request.user
		user_profile, up_created = UserProfile.objects.get_or_create(user = user)

		post = request.POST.copy()

		if post['type'] == 'artist':
			print "type: artist "
			artist_name = post['artist_name']
			artist_id = post['artist_id']
			artist = get_or_create_artist_by_mbid(artist_id)


			if artist in user_profile.artists.all():
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

			label = get_or_create_label_by_mbid(label_id)

			if label in user_profile.labels.all():
				user_profile.labels.remove(label)
				user_profile.save()
				print "unfollowed label"

			else:
				user_profile.labels.add(label)
				user_profile.save()
				print "followed label"


		elif post['type'] == 'track':
			print "type: track "
			track_id = post['track_id']
			artist_name = post['artist']
			artist_id = post['artist_id']
			title = post['title']
			print track_id
			track = get_or_create_recording(title = title, artist_name = artist_name, mbid = track_id)

			# if user_profile.sounds.filter(mbid = track_id).exists():
			if track in user_profile.sounds.all():
				user_profile.sounds.remove(track)
				user_profile.save()
				print "unfollowed sound"

			else:
				user_profile.sounds.add(track)
				user_profile.save()
				print "followed sound"

		elif post['type'] == 'album':
			print "type: album"
			reid = post['reid']
			artist_name = post['artist']
			title = post['title']
			release = get_or_create_release(title = title, artist_name = artist_name, reid = reid)

			if release in user_profile.albums.all():
			# if user_profile.albums.filter(reid = reid).exists():
				user_profile.albums.remove(release)
				user_profile.save()
				print "unfollowed album"

			else:
				user_profile.albums.add(release)
				user_profile.save()
				print "followed album"


		return HttpResponse("you're logged in!! " + request.user.username)
	else:
		return HttpResponse('You must be logged in to do this', status=401)

def follow_album(request):
	if request.user.is_authenticated():
		user = request.user
		user_profile, up_created = UserProfile.objects.get_or_create(user = user)

		post = request.POST.copy()


		if post['type'] == 'album':
			print "type: album"
			reid = post['reid']
			artist_name = post['artist']
			title = post['title']
			release = get_or_create_release(title = title, artist_name = artist_name, reid = reid)

			if user_profile.albums.filter(reid = reid).exists():
				user_profile.albums.remove(release)
				user_profile.save()
				print "unfollowed album"

			else:
				user_profile.albums.add(release)
				user_profile.save()
				print "followed album"


		return HttpResponse("you're logged in!! " + request.user.username)
	else:
		return HttpResponse('You must be logged in to do this', status=401)



def check_if_follows(request, model_type, list_of_entities):
	if request.user.is_authenticated():
		user_profile, up_created = UserProfile.objects.get_or_create(user = request.user)
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
		 		matches = model_entries.filter(artists__name__iexact =item['artist'], title__iexact = item['title'])
		 		artist_name_matches = model_entries.filter(artist_name__iexact =item['artist'], title__iexact = item['title'])
		 		if (matches or artist_name_matches) or ('track_id' in item and item['track_id'] in mbids) or ('mbid' in item and item['mbid'] in mbids):
		 			item['following_sound'] = True
		 			print "following sound"
		 		# elif 'track_id' in item and item['track_id'] in mbids:
		 		# 	# item['following_sound'] = "You Like This"
		 		# 	item['following_sound'] = True
		 		# 	print "following sound"
		 		# elif 'mbid' in item and item['mbid'] in mbids:
		 		# 	# item['following_sound'] = "You Like This"
		 		# 	item['following_sound'] = True
		 		# 	print "following sound"
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
		 		artist_name_matches = model_entries.filter(artist_name__iexact =item['artist'], title__iexact = item['title'])
		 		if artist_name_matches or matches:
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







def remove_user_playlist(request):
	if request.user.is_authenticated():
		user = request.user
		user_profile, up_created = UserProfile.objects.get_or_create(user = user)
		if 'playlist_id' in request.POST:
			playlist = User_playlist.objects.get(pk =request.POST['playlist_id'])
			if playlist in user_profile.user_playlists.all():
				playlist.delete()
				return HttpResponse('success')
			else:
				return HttpResponse("You don't have permission to delete this",  status=401)
		else:
			return HttpResponse("no playlist ID passed",  status=400)
	else:
		return HttpResponse("You must be logged in to delete playlists",  status=401)


def delete_playlist_entry(request):
	if request.user.is_authenticated():
		user = request.user
		user_profile, up_created = UserProfile.objects.get_or_create(user = user)
		if 'entry_id' in request.POST:
			entry = User_playlist_entry.objects.get(pk =request.POST['entry_id'])
			playlist = entry.user_playlist
			if user_profile in playlist.users.all():
				entry.delete()
				return HttpResponse('success')
			else:
				return HttpResponse("You don't have permission to delete this",  status=401)
		else:
			return HttpResponse("no entry ID recieved",  status=400)
	else:
		return HttpResponse("You must be logged in to edit playlists",  status=401)




def get_user_playlists(user):
	user_profile, up_created = UserProfile.objects.get_or_create(user = user)
	playlist_set = user_profile.user_playlists.all()
	playlists = []
	for entry in playlist_set:
		playlist = {"name":entry.name, "pk":entry.pk,'description':entry.description}
		playlists.append(playlist)
	return playlists


def get_playlists(request):
	if request.user.is_authenticated():
		user = request.user

		playlists = get_user_playlists(user)		
		results = {'playlists':playlists}

		return_json = simplejson.dumps(results)
		return HttpResponse(return_json, mimetype='application/json')
	else:
		return HttpResponse("You need to be logged in to make playlists", status=401)




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
	title = get["title"]

	tracks = lastfmAlbumTracklist(artist, title)
	tracks = check_if_follows(request,'sounds', tracks)

	print "this are the tracks from get album tracks from lastfm"
	print tracks
	results = {'tracks':tracks}
	#results = {"reid":reid, 'tracks':tracks}
	return_json = simplejson.dumps(results)
	return HttpResponse(return_json, mimetype='application/json')
		#return HttpResponse("album page!!!")
	# else:
	# 	return HttpResponse('You must be logged in to do this', status=401)

lastfm_api_key = "c43db4e93f7608bb10d96fa5f69a74a1"

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
			try:
				mbid = post['mbid']
			except:
				mbid = ""
			artist_name = post['artist_name']
			sound = get_or_create_recording(title = title, artist_name = artist_name, mbid = mbid)
			playlist_id = post['playlist_id']
			playlist = User_playlist.objects.get(pk =playlist_id)

			playlist_entry = User_playlist_entry(sound = sound, user_playlist = playlist)
			playlist_entry.save()

		return HttpResponse('success')
	else:
		return HttpResponse("You need to be logged in to make playlists",  status=401)


import json

def check_track_ajax(request):
	if request.POST:
		sounds = request.POST['tracks']
		sounds = json.loads(sounds)
		# sounds = [track]
		print "check_track_ajax tracks:", sounds, type(sounds)
		sounds = check_if_follows(request, 'sounds', sounds)

		results = {'sounds':sounds}
		#results = {"reid":reid, 'tracks':tracks}
		return_json = simplejson.dumps(results)
		return HttpResponse(return_json, mimetype='application/json')
	else:
		return HttpResponse("No POST data received",  status=400)












