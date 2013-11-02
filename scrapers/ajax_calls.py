from scrapers.mbz_module import *
from scrapers.db_handler import *
from external_APIs import *

import simplejson

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

