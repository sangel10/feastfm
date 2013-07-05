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

def home(request):
	if request.GET:
		get = request.GET.copy()
		username = get['username']
		lastfm_api_key = "c43db4e93f7608bb10d96fa5f69a74a1"
		url = "http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user="+username+"&api_key="+lastfm_api_key+"&format=json&limit=150"
		print url
		data = urllib2.urlopen(url)
		data = json.load(data)
		artists = []
		for artist in data["topartists"]["artist"]:
			artists.append(artist["name"])
		# artists = ["Boards of Canada", "Vampire Weekend", "Four Tet", "Hot Chip", "James Blake", "The Knife", "Tricky", "The National", "Radiohead", "Prince",]
		release_results = get_mbz_releases(artists)
		rgids = []
		releases = []
		for release in release_results:
			try:
				if release["release-group"]["id"] in rgids:
					continue
				else:
					artist = release['artist-credit'][0]['artist']['name']
					title = release["title"]
					reid = release["id"]
					date = release['date']
					rgids.append(release["release-group"]["id"])
					try:
						label = release['label-info'][0]['label']['name']
					except:
						label = ""
					try:
						cat_num = release['label-info'][0]['catalog-number']
					except:
						cat_num = ""
					if artist in artists:
						releases.append({"artist":artist, "title":title, "reid":reid, 'date':date, 'label':label, 'cat_num':cat_num})
					# 	releases.append(artist+" - "+title)
			except:
				continue #should this be 'pass'?


		#return HttpResponse("Username found: %s" % username )
		return render_to_response('scrapers/home.html',{'artists':artists, 'releases':releases},context_instance=RequestContext(request))
		# call username API
		# send to template that charts out each 
	else:
		#return HttpResponse("No username")
		return render_to_response('scrapers/home.html')



def get_mbz_releases(artists):
	today = datetime.date.today()
	last_month = today - datetime.timedelta(days=100)
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
	releases = []
	offset = 0
	#while True:
	url = "http://www.musicbrainz.org/ws/2/release?&query="+ query+ "&limit=100&fmt=json&offset="+str(offset)
	#url = urllib.quote_plus(url)
	data = urllib2.urlopen(url)
	api_results = json.load(data)
	releases = releases + api_results["releases"]
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



