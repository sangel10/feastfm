from scrapers.models import *
from scrapers.mbz_module import *
from django.http import HttpResponse
from django.shortcuts import render_to_response
import datetime
from django.template import RequestContext

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


def get_or_create_recording(title = '', artist_name = '', mbid =''):
	if mbid:
		recording = get_or_create_recording_by_mbid(mbid)
		return recording
	elif title and artist_name:
		recording, created = Sound.objects.get_or_create(title = title, artist_name = artist_name)
		return recording
	else:
		print "Error, get_or_create_release requires either an MBID or a title and an artist_name"



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

			if user_profile.sounds.filter(mbid = track_id).exists():
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


# def follow_album(request):
# 	if request.user.is_authenticated():
# 		user = request.user
# 		user_profile, up_created = UserProfile.objects.get_or_create(user = user)

# 		post = request.POST.copy()
# 		post_type = post['type']
# 		print post_type
# 		if post_type == 'album':
# 			print "type: album "
# 			# artist_name = post['artist_name']
# 			# print artist_name 
# 			artist_name = post['artist']
# 			title = post['title']
# 			reid = post['reid']

# 			album = get_or_create_release(artist_name = artist_name, title = title, reid=reid)
# 			# artist = get_artist_by_mbid(artist_id)


# 			if album in user_profile.albums.all():
# 				user_profile.albums.remove(album)
# 				user_profile.save()
# 				print "unfollowed album"

# 			else:
# 				user_profile.albums.add(album)
# 				user_profile.save()
# 				print "followed album"

# 		return HttpResponse("you're logged in!! " + request.user.username)
# 	else:
# 		return HttpResponse('You must be logged in to do this', status=401)


