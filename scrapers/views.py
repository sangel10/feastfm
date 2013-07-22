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

#@login_required(login_url='/accounts/login/')
def home(request):
	if request.GET:
		get = request.GET.copy()
		username = get['username']
		artists = get_lastfm_artists(username, 100)
		# artists = ["Boards of Canada", "Vampire Weekend", "Four Tet", "Hot Chip", "James Blake", "The Knife", "Tricky", "The National", "Radiohead", "Prince",]
		artist_names = []
		for artist in artists:
			artist_names.append(artist['name'])
		query = get_stream_query(artist_names)
		#api_results = artist_names_query(artists)
		# rgids = []
		# releases = []
		releases = get_browse_releases('stream', query)
		# parsed_results = parse_releases({'releases':api_results}, rgids)
		# releases += parsed_results['releases']
		# rgids += parsed_results['rgids']
		# for release in release_results:
		# 	try:
		# 		if release["release-group"]["id"] in rgids:
		# 			continue
		# 		else:
		# 			artist = release['artist-credit'][0]['artist']['name']
		# 			artist_id = release['artist-credit'][0]['artist']['id']
		# 			title = release["title"]
		# 			reid = release["id"]
		# 			date = release['date']
		# 			rgid = release["release-group"]["id"]
		# 			rgids.append(rgid)
		# 			try:
		# 				label = release['label-info'][0]['label']['name']
		# 				label_id = release['label-info'][0]['label']['id']
		# 			except:
		# 				label = ""
		# 				label_id = ""
		# 			try:
		# 				cat_num = release['label-info'][0]['catalog-number']
		# 			except:
		# 				cat_num = ""
		# 			try:
		# 				primary_type = release['release-group']['primary-type']
		# 			except:
		# 				primary_type = ""
		# 			try:
		# 				secondary_types = release['release-group']['secondary-types'][0]
		# 			except:
		# 				secondary_types = ""
		# 			if artist in artists:
		# 				releases.append({
		# 					"artist":artist, 
		# 					"title":title, 
		# 					"reid":reid,
		# 					'rgid':rgid,
		# 					'date':date, 
		# 					'label':label, 
		# 					'cat_num':cat_num, 
		# 					'primary_type':primary_type, 
		# 					'secondary_types':secondary_types,
		# 					'artist_id': artist_id,
		# 					'label_id':label_id,
		# 					})
			# except:
			# 	continue #should this be 'pass'?


		#return HttpResponse("Username found: %s" % username )
		return render_to_response('scrapers/home.html',{'page':'home', 'releases':releases},context_instance=RequestContext(request))
		# call username API
		# send to template that charts out each 
	else:
		#return HttpResponse("No username")
		return render_to_response('scrapers/home.html', {'page':'start'})

def get_lastfm_artists(username, number):
		lastfm_api_key = "c43db4e93f7608bb10d96fa5f69a74a1"
		limit = number
		url = "http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user="+username+"&api_key="+lastfm_api_key+"&format=json&limit="+str(limit)
		print url
		data = urllib2.urlopen(url)
		data = json.load(data)
		artists = []
		for artist in data["topartists"]["artist"]:
			artists.append({"name":artist["name"], "mbid":artist['mbid']})
		return artists

def get_stream_query(artists):
	today = datetime.date.today()
	last_month = today - datetime.timedelta(days=60)
	end_date = today.strftime('%Y-%m-%d')
	start_date = last_month.strftime('%Y-%m-%d')

	query = 'date:['+start_date +" TO "+ end_date+']'
	query += "AND("
	for artist in artists:
		if artists.index(artist) == 0:
			query = query + 'artist: "' + artist + '"'
		else:
			query = query + ' OR artist:"' + artist + '"'

	query += ')'
	query = urllib.quote_plus(query.encode('utf8'))
	print query
	return query 
	# releases = []
	# offset = 0
	# #while True:
	# url = "http://www.musicbrainz.org/ws/2/release?&query="+ query+ "&limit=100&fmt=json&offset="+str(offset)
	# #url = urllib.quote_plus(url)
	# data = urllib2.urlopen(url)
	# api_results = json.load(data)
	# releases = releases + api_results["releases"]
		# offset +=1
		# if not api_results["releases"]:
		# 	break
		
	return releases

def get_album_tracks(request):
	get = request.GET.copy()
	reid = get["reid"]
	url = "http://www.musicbrainz.org/ws/2/release/"+reid+"?fmt=json&inc=artist-credits+recordings"
	data = urllib2.urlopen(url)
	api_results = json.load(data)
	tracks = []
	for entry in api_results['media']:
		for track in entry['tracks']:
			artist = track['artist-credit'][0]['name']
			title = track['title']
			tracks.append({'artist':artist, 'title':title})
	# results = {'reid':reid, 'tracks':tracks}
	results = {'test':"is this working?", "reid":reid, 'tracks':tracks}
	return_json = simplejson.dumps(results)
	return HttpResponse(return_json, mimetype='application/json')
	#return HttpResponse("album page!!!")


def artist(request, artist_id):
	url = "http://www.musicbrainz.org/ws/2/release-group/?query=arid:"+artist_id+"&fmt=json"
	data = urllib2.urlopen(url)
	api_results = json.load(data)
	releases = []
	for release in api_results['release-groups']:
		title = release['title']
		rgid = release['id']
		artist = release['artist-credit'][0]['artist']['name']
		reid = release['releases'][0]['id']
		release_status = release['releases'][0]['status']
		releases.append({
			'title':title, 
			'rgid':rgid,
			'artist':artist,
			'reid':reid,
			})
	return render_to_response('scrapers/home.html',{'page':'artist', 'releases':releases})
	#return HttpResponse("artist id: " +artist_id)

def artist_browse(request, artist_id):
	releases = get_browse_releases('artist', artist_id)
	# offset = 0 
	# releases = []
	# rgids = []
	# while True:
	# 	url = "http://www.musicbrainz.org/ws/2/release?artist="+artist_id+"&fmt=json&limit=100&offset="+str(offset)+"&inc=artist-credits+release-groups+labels"
	# 	data = urllib2.urlopen(url)
	# 	api_results = json.load(data)
	# 	offset +=100
	# 	if api_results["releases"] == []:
	# 		break
	# 	for release in api_results['releases']:
	# 		rgid = release['release-group']['id']
	# 		if rgid in rgids:
	# 			continue
	# 		date = release['release-group']['first-release-date']
	# 		title = release['title']
	# 		artist = release['artist-credit'][0]['artist']['name']
	# 		artist_id = release['artist-credit'][0]['artist']['id']
	# 		reid = release['id']
	# 		#release_status = release['status']
	# 		primary_type = release['release-group']['primary-type']
	# 		secondary_types = release['release-group']['secondary-types']
	# 		try:
	# 			label = release['label-info'][0]['label']['name']
	# 			label_id = release['label-info'][0]['label']['id']
	# 			cat_num = release['label-info'][0]['catalog-number']
	# 		except:
	# 			label = ""
	# 			label_id = ""
	# 			cat_num = ""
	# 		rgids.append(rgid)
	# 		releases.append({
	# 			'title':title, 
	# 			'rgid':rgid,
	# 			'artist':artist,
	# 			'artist_id':artist_id,
	# 			'reid':reid,
	# 			'date':date,
	# 			'primary_type':primary_type,
	# 			'secondary_types':secondary_types,
	# 			'label':label,
	# 			'label_id':label_id,
	# 			'cat_num':cat_num,
	# 			})
	return render_to_response('scrapers/home.html',{'page':'artist', 'releases':releases})
	#return HttpResponse("artist id: " +artist_id)




def label(request, label_id):
	releases = get_browse_releases('label', label_id)
	# offset = 0
	# releases = []
	# rgids = []
	# while True:
	# 	url = "http://www.musicbrainz.org/ws/2/release?label="+label_id+"&fmt=json&limit=100&offset="+str(offset)+"&inc=artist-credits+release-groups+labels"
	# 	data = urllib2.urlopen(url)
	# 	api_results = json.load(data)
	# 	offset +=100
	# 	if api_results["releases"] == []:
	# 		break
	# 	for release in api_results['releases']:
	# 		rgid = release['release-group']['id']
	# 		if rgid in rgids:
	# 			continue
	# 		date = release['date']
	# 		title = release['title']
	# 		artist = release['artist-credit'][0]['artist']['name']
	# 		artist_id = release['artist-credit'][0]['artist']['id']
	# 		reid = release['id']
	# 		# cat_num = release['label-info'][0]['catalog-number']
	# 		primary_type = release['release-group']['primary-type']
	# 		secondary_types = release['release-group']['secondary-types']
	# 		rgids.append(rgid)
	# 		try:
	# 			label = release['label-info'][0]['label']['name']
	# 			label_id = release['label-info'][0]['label']['id']
	# 			cat_num = release['label-info'][0]['catalog-number']
	# 		except:
	# 			label = ""
	# 			label_id = ""
	# 			cat_num = ""
	# 		releases.append({
	# 			'date':date,
	# 			'title':title,
	# 			'artist':artist,
	# 			'artist_id':artist_id,
	# 			'rgid':rgid,
	# 			'reid':reid,
	# 			'cat_num':cat_num,
	# 			'primary_type':primary_type,
	# 			'secondary_types':secondary_types,
	# 			'label':label,
	# 			'label_id':label_id,
	# 			})
		
	#return render_to_response('scrapers/home.html',{'page':'label', 'releases':releases})
	#return HttpResponse("label id: " +label_id)
	return render_to_response('scrapers/home.html',{'page':'label', 'releases':releases})



def get_browse_releases(query_type, mbid):
	offset = 0
	releases = []
	rgids = []
	while True:
		if query_type == 'label':
			url = "http://www.musicbrainz.org/ws/2/release?label="+mbid+"&fmt=json&limit=100&offset="+str(offset)+"&inc=artist-credits+release-groups+labels"
		if query_type == 'artist':
			url = "http://www.musicbrainz.org/ws/2/release?artist="+mbid+"&fmt=json&limit=100&offset="+str(offset)+"&inc=artist-credits+release-groups+labels"
		if query_type == 'stream':
			url = "http://www.musicbrainz.org/ws/2/release?&query="+mbid+ "&limit=100&fmt=json&offset="+str(offset)
		data = urllib2.urlopen(url)
		api_results = json.load(data)
		if api_results["releases"] == []:
			break
		parsed_results = parse_releases(api_results, rgids)
		releases += parsed_results['releases']
		rgids += parsed_results['rgids']
		offset +=100
	#return render_to_response('scrapers/home.html',{'page':query_type, 'releases':releases})
	return releases	


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

def search():
	pass

def search_by_lastfm():
	if request.GET:
		get = request.GET.copy()
		username = get['username']
		artists = get_lastfm_artists(username, 500)
		# query = 
		# for artist in artists:

def mbz_artists_query():
	pass



