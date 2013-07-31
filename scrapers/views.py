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


sc_client_id = 'a0b4638bae6d50a9296f7fc3f35442eb'



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

def get_stream_query(query_type, mbids):
	# query_type = 'artist'
	today = datetime.date.today()
	last_month = today - datetime.timedelta(days=30)
	end_date = today.strftime('%Y-%m-%d')
	start_date = last_month.strftime('%Y-%m-%d')

	if query_type == 'artist' or 'label':
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
	# else:
	# 	return HttpResponse('You must be logged in to do this', status=401)


def artist_browse(request, artist_id):
	releases, rgids = get_browse_releases('artist', artist_id)
	return render_to_response('scrapers/home.html',{'page':'artist', 'releases':releases}, context_instance=RequestContext(request))
	#return HttpResponse("artist id: " +artist_id)




def label(request, label_id):
	releases, rgids = get_browse_releases('label', label_id)
	#return render_to_response('scrapers/home.html',{'page':'label', 'releases':releases})
	#return HttpResponse("label id: " +label_id)
	return render_to_response('scrapers/home.html',{'page':'label', 'releases':releases}, context_instance=RequestContext(request))



def get_browse_releases(query_type, mbid_or_query, rgids = None):
	offset = 0
	releases = []
	if rgids == None:
		rgids = []
	while True:
		if query_type == 'label':
			url = "http://www.musicbrainz.org/ws/2/release?label="+mbid_or_query+"&fmt=json&limit=100&offset="+str(offset)+"&inc=artist-credits+release-groups+labels"
		if query_type == 'artist':
			url = "http://www.musicbrainz.org/ws/2/release?artist="+mbid_or_query+"&fmt=json&limit=100&offset="+str(offset)+"&inc=artist-credits+release-groups+labels"
		if query_type == 'stream':
			url = "http://www.musicbrainz.org/ws/2/release?&query="+mbid_or_query+ "&limit=100&fmt=json&offset="+str(offset)
		print "THIS IS THE QUERY URL: \n" + url
		data = urllib2.urlopen(url)
		api_results = json.load(data)
		if api_results["releases"] == []:
			break
		parsed_results = parse_releases(api_results, rgids)
		releases += parsed_results['releases']
		rgids += parsed_results['rgids']
		offset +=100
	#return render_to_response('scrapers/home.html',{'page':query_type, 'releases':releases})
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
		artists = get_lastfm_artists(username, 100)
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

	# query_type = 'artist'
	query = get_stream_query(query_type, names)
	api_results = mbz_search(query, query_type)
	print "results search sees: "
	print api_results
	results = []
	if query_type == 'label':
		# query_type = 'labels'
		for entry in api_results['labels']:
			print "api_results length: " + str(len(api_results))
			# print "ENTRY: "
			# print entry 
			results.append({'name':entry['name'], 'mbid':entry['id']})
		return render_to_response('scrapers/home.html',{'page':'soundcloud', 'labels':results},context_instance=RequestContext(request))
	elif query_type == 'artist':
		for entry in api_results['artist']:
			results.append({'name':entry['name'], 'mbid':entry['id']})
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
				print "api_results length: " + str(len(api_results))
				# print "ENTRY: "
				# print entry 
				results.append({'name':entry['name'], 'mbid':entry['id']})
			return render_to_response('scrapers/home.html',{'page':'search', 'labels':results},context_instance=RequestContext(request))
		elif query_type == 'artist':
			for entry in api_results['artist']:
				results.append({'name':entry['name'], 'mbid':entry['id']})
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


def follow_toggle(request):
	if request.user.is_authenticated():
		user = request.user
		user_profile, up_created = UserProfile.objects.get_or_create(user = user)

		post = request.POST.copy()

		if post['type'] == 'artist':
			print "type: artist "
			# artist_name = post['artist_name']
			# print artist_name 
			artist_id = post['artist_id']
			print artist_id
			# artist_name = get_english_alias(artist_id)
			artist, artist_created = Artist.objects.get_or_create(mbid = artist_id)
			print artist 
			if artist_created:
				artist.name = get_english_alias('artist', artist_id)
				artist.save()
				print "added artist"

			if user_profile.artists.filter(mbid = artist_id).exists():
				user_profile.artists.remove(artist)
				user_profile.save()
				print "unfollowed artist"

			else:
				user_profile.artists.add(artist)
				user_profile.save()
				print "followed artist"


		if post['type'] == 'label':
			print "type: label "
			label_id = post['label_id']
			print label_id
			# artist_name = get_english_alias(artist_id)
			label, label_created = Label.objects.get_or_create(mbid = label_id)
			print label 
			if label_created:
				label.name = get_english_alias('label', label_id)
				label.save()
				print "added label"

			if user_profile.labels.filter(mbid = label_id).exists():
				user_profile.labels.remove(label)
				user_profile.save()
				print "unfollowed label"

			else:
				user_profile.labels.add(label)
				user_profile.save()
				print "followed label"

		return HttpResponse("you're logged in!! " + request.user.username)
	else:
		return HttpResponse('You must be logged in to do this', status=401)

	
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

		query = get_stream_query('arid', artist_ids)
		new_releases, new_rgids = get_browse_releases('stream', query, rgids)
		releases +=new_releases
		rgids+= new_rgids

		query = get_stream_query('laid', label_ids)
		new_releases, new_rgids = get_browse_releases('stream', query, rgids)
		releases +=new_releases
		rgids+= new_rgids

		return render_to_response('scrapers/home.html',{'page':'stream', 'releases':releases}, context_instance=RequestContext(request))

	else:
		return HttpResponse("You need to be logged in to have a stream")

