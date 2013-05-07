import urllib2
import lxml 
from bs4 import BeautifulSoup
import json
from pprint import pprint
import feedparser
import inspect

url = 'http://www.factmag.com/2013/04/05/download-major-lazers-fourth-lazer-strikes-back-ep/'
client_id = "a0b4638bae6d50a9296f7fc3f35442eb"

# last.fm
last_fm_api_key = "c43db4e93f7608bb10d96fa5f69a74a1"
# Secret: is e93504ee9bad8ec5966d1db1f26a4cd0

echo_nest_API_key = "FBHCMLQRHBCWD8GVA"

def make_soup(url):
	print inspect.stack()[0][3]
	data = urllib2.urlopen(url)
	soup = BeautifulSoup(data)
	return soup

def find_soundcloud(soup):
	print inspect.stack()[0][3]
	results = []
	iframes = soup.find_all("iframe")
	for frame in iframes:
		src = frame.get("src")
		if src.find("soundcloud.com/player") != -1:
			src = src.split("?")[1]
			if src.find("playlists")!= -1 and src.find("sharing=false") == -1:
				src = src.split("playlists%2F")[1]
				src = src.split("&")[0]
				src = src.split("%3F")[0]
				results.append({"type":"playlist", "link":src})
			if src.find("tracks")!= -1:
				src = src.split("tracks%2F")[1]
				src = src.split("&")[0]
				src = src.split("%3F")[0]
				results.append({"type":"track", "link":src})
	return results

def find_youtube(soup):
	print inspect.stack()[0][3]
	results = []
	iframes = soup.find_all("iframe")
	for frame in iframes:	
		src = frame.get("src")
		if src.find("youtube.com/embed") != -1:
			if src.find("list") != -1:
				src = src.split("list=")[1]
				src = src.split("&amp")[0]
				src = src.split("&")[0]
				results.append({"type":"playlist", "link":src})
			else:
				src =src.split("embed/")[1]
				src = src.split("?")[0]
				results.append({"type":"track","link":src})
	objs = soup.find_all("object")
	for o in objs:
		if o.src:
			src = o.get("src")
			if src.find("youtube.com/v/") != -1:
				src =src.split("/v/")[1]
				src = src.split("?")[0]
				results.append({"type": track, "link":src})
	return results

def find_vimeo(soup):
	print inspect.stack()[0][3]
	results = []
	iframes = soup.find_all("iframe")
	for frame in iframes:
		src = frame.get("src")
		if src.find("player.vimeo") != -1:
			src = src.split("video/")[1]
			src = src.split("?")[0]
			results.append({"type":"track", "link":src})
	return results

def get_vimeo_track(track_id):
	print inspect.stack()[0][3]
	track_id = str(track_id)
	vimeo_url = "http://vimeo.com/api/v2/video/"+track_id+".json"
	track_data = urllib2.urlopen(vimeo_url)
	track_data = json.load(track_data)
	track_dict = process_vimeo_track(track_data)
	tracks = []
	tracks.append(track_dict)
	return {"tracks":tracks, "playlists":[]}
	#return track_data

def process_vimeo_track(track_data):
	print inspect.stack()[0][3]
	title = track_data[0]["title"]
	username = track_data[0]["user_name"]
	vimeo_track_id = track_data[0]["id"]
	length = track_data[0]["duration"]
	track_dict = {"title":title, "vimeo_username":username, "vimeo_track_id":vimeo_track_id, "length":length}
	return track_dict


def get_SC_track(track_id):
	print inspect.stack()[0][3]
	track_id = str(track_id)
	#client_id = "a0b4638bae6d50a9296f7fc3f35442eb"
	SC_track_url = "http://api.soundcloud.com/tracks/"+track_id+".json?client_id="+client_id
	try:
		track_data = urllib2.urlopen(SC_track_url)
		track_data = json.load(track_data)
		track_dict = process_SC_track(track_data)
		tracks = []
		tracks.append(track_dict)
		return {"tracks":tracks,"playlists":[]}
	except Exception, e:
		print e
		return {"tracks":[],"playlists":[]}

#separated retrieving data from the API and processing the data in order to 
#have data processing form a single track and from multiple playlist entries all in one function

def process_SC_track(track_data):
	print inspect.stack()[0][3]
	title = track_data["title"]
	user_id = track_data["user"]["id"]
	soundcloud_track_id = track_data["id"]
	#
	release = track_data["release"]
	label = track_data["label_name"]
	length = track_data["duration"]
	#
	track_dict = {"title": title, "sc_track_id": soundcloud_track_id, "sc_release":release, "sc_label":label, "length":length}
	#track_dict = {"title": title, "track_id": track_id}
	user_data = get_SC_user(user_id)
	track_dict.update(user_data)
	return track_dict

def process_SC_playlist(playlist_data):
	print inspect.stack()[0][3]
	SC_playlist_id = ""
	SC_playlist_id = playlist_data["id"]
	tracklist = []
	for track in playlist_data["tracks"]:
		track_id = track["id"]
		tracklist.append(track_id)
	return {"sc_playlist_id": SC_playlist_id, "tracklist":tracklist}
	# processed_playlist = {"SC_playlist_id":SC_playlist_id, "tracklist":tracklist}
	# return processed_playlist



def get_SC_playlist(playlist_id):
	print inspect.stack()[0][3]
	playlists = []
	tracks = []
	playlist_id = str(playlist_id)
	#client_id = "a0b4638bae6d50a9296f7fc3f35442eb"
	SC_playlist_url = "http://api.soundcloud.com/playlists/"+playlist_id+".json?client_id="+client_id
	try:
		playlist_data = urllib2.urlopen(SC_playlist_url)
		playlist_data = json.load(playlist_data)
		playlist_dict = process_SC_playlist(playlist_data)
		#print "THIS IS WHAT PROCESS SC PLAYLIST RETURNS: %r" %playlist_dict
		playlists.append(playlist_dict)
		#return playlist_data
		for track in playlist_data["tracks"]:
			track_dict = process_SC_track(track)
			tracks.append(track_dict)
		results = {"tracks":tracks, "playlists":playlists}
		return results
	except Exception, e:
		print e
		return {"tracks":[],"playlists":[]}

def get_SC_user(user_id):
	print inspect.stack()[0][3]
	user_id = str(user_id)
	#client_id = "a0b4638bae6d50a9296f7fc3f35442eb"
	SC_user_url = "http://api.soundcloud.com/users/"+user_id+".json?client_id="+client_id
	user_data = urllib2.urlopen(SC_user_url)
	user_data = json.load(user_data)
	username = user_data["username"]
	full_name = user_data["full_name"]
	return {"sc_username": username, "sc_full_name": full_name}

def get_YT_track(track_id):
	print inspect.stack()[0][3]
	url = "https://gdata.youtube.com/feeds/api/videos/"+track_id+"?v=2&alt=json"
	track_data = urllib2.urlopen(url)
	track_data = json.load(track_data)
	entry = track_data["entry"]
	track_dict = process_YT_track(entry)
	tracks = []
	tracks.append(track_dict)
	return {"tracks":tracks, "playlists":[]}

#separated retrieving data from the API and processing the data in order to 
#have data processing form a single track and from multiple playlist entries all in one function

def process_YT_track(entry):
	print inspect.stack()[0][3]
	title = entry["title"]["$t"]
	length = entry['media$group']['yt$duration']['seconds']
	YT_track_id = entry["media$group"]["yt$videoid"]["$t"]
	track_dict = {"title":title, "length":length, "yt_track_id":YT_track_id}
	return track_dict

def process_YT_playlist(playlist_data):
	print inspect.stack()[0][3]
	YT_playlist_id = playlist_data["feed"]["yt$playlistId"]["$t"]
	tracklist = []
	for entry in playlist_data["feed"]["entry"]:
		track_id = entry["media$group"]["yt$videoid"]["$t"]
		tracklist.append(track_id)
	processed_playlist = {"yt_playlist_id":YT_playlist_id,"tracklist":tracklist}
	return processed_playlist

def get_YT_playlist(playlist_id):
	print inspect.stack()[0][3]
	url = "https://gdata.youtube.com/feeds/api/playlists/"+playlist_id+"?v=2&alt=json"
	playlist_data = urllib2.urlopen(url)
	playlist_data = json.load(playlist_data)
	processed_playlist = process_YT_playlist(playlist_data)
	entries = playlist_data["feed"]["entry"]
	tracks = []
	for entry in entries:
		# title = entry["title"]["$t"]
		# tracks.append(title)
		# YT_track_id = entry["media$group"]["yt$videoid"]["$t"]
		# track = get_YT_track(YT_track_id)
		track = process_YT_track(entry)
		tracks.append(track)
	return {"tracks":tracks, "playlists":processed_playlist}

def scrape(url):
	print inspect.stack()[0][3]
	YT = []
	SC = []	
	vimeo = []
	soup = make_soup(url)
	SC = find_soundcloud(soup)
	YT = find_youtube(soup)
	vimeo = find_vimeo(soup)
	results = {"tracks":[], "playlists":[]}
	tracks = []
	playlists = []
	for track in vimeo:
		if track["type"] == "track":
			data = get_vimeo_track(track["link"])
			#results = update_results(results, data)
			playlists = playlists +data["playlists"]
			tracks = tracks + data["tracks"]
	for track in SC:
		if track["type"] == "playlist":
			data = get_SC_playlist(track["link"])
			#results = update_results(results, data)
			playlists = playlists +data["playlists"]
			tracks = tracks + data["tracks"]
		if track["type"] == "track":
			data = get_SC_track(track["link"])
			#results = update_results(results, data)
			playlists = playlists +data["playlists"]
			tracks = tracks + data["tracks"]
	for track in YT:
		if track["type"] == "playlist":
			data = get_YT_playlist(track["link"])
			#results = update_results(results, data)
			playlists = playlists +data["playlists"]
			tracks = tracks + data["tracks"]
		if track["type"] == "track":
			data = get_YT_track(track["link"])
			#results = update_results(results, data)
			playlists = playlists +data["playlists"]
			tracks = tracks + data["tracks"]
	return {"tracks":tracks, "playlists":playlists}
	#return results

def update_results(results, data):
	print inspect.stack()[0][3]
	for entry in data["tracks"]:
		print "This is a track entry: %r" %entry
		results["tracks"].append(entry)
	for entry in data["playlists"]:
		print "this is a playlist entry %r" %entry
		results["playlists"].append(entry)
	return results


factmag = "http://feeds.feedburner.com/FactMagazineMusicAndArt?fmt=xml"
LWE = "http://feeds.feedburner.com/littlewhiteearbuds/gKeY?fmt=xml"
xlr8r = "http://feeds.feedburner.com/xlr8rnews?format=xml"

mthrfnkr = "http://mthrfnkr.fm/feed/"
pitchfork_tracks = "http://pitchfork.com/rss/reviews/tracks/"
pitchfork_best_tracks = "http://pitchfork.com/rss/reviews/best/tracks/"

feeds = [factmag, LWE, xlr8r, mthrfnkr, pitchfork_tracks, pitchfork_best_tracks]

# def scrape_feed(site):
# 	print inspect.stack()[0][3]
# 	results = {"tracks" : [], "playlists":[]}
# 	feed = feedparser.parse(site)
# 	for entry in feed.entries:
# 		rss_data = get_RSS_json(entry)
# 		url = rss_data["url"]
# 		print url
# 		scrape_results = scrape(url)
# 		print scrape_results
# 		for item in scrape_results["tracks"]:
# 			results["tracks"].append(item)
# 		for item in scrape_results["playlists"]:
# 			results["playlists"].append(item)
# 	pprint(results)


def scrape_feed(site):
	print inspect.stack()[0][3]
	print __name__
	results = {"tracks":[],"playlists":[]}
	feed = feedparser.parse(site)
	source = feed.feed.link
	for entry in feed.entries:
		rss_data = get_RSS_json(entry)
		rss_data["source"] = source
		url = rss_data["url"]
		print url
		track_results = scrape(url)
		print "This is what scrape_all sees: "
		pprint(track_results)
		#print track_results
		# print "Tracks: " track_results["tracks"]
		# print "Playlists: " track_results["playlists"]
		for sound in track_results["tracks"]:
			sound.update(rss_data)
		for sound in track_results["playlists"]:
			sound.update(rss_data)
		results = update_results(results, track_results)
	#pprint(results)
	return results


def scrape_all(RSSfeeds):
	print inspect.stack()[0][3]
	#results = {"tracks":[],"playlists":[]}
	tracks = []
	playlists = []
	for site in RSSfeeds:
		feed_results = scrape_feed(site)
		#results = update_results(results,feed_results)
		if feed_results != None:
			tracks = tracks + feed_results["tracks"]
			playlists = playlists + feed_results["playlists"]
	results= {"tracks":tracks,"playlists":playlists}
	#print "these are the final results: !!!   "
	#return pprint(results)
	return results


def get_RSS_json(entry):
	print inspect.stack()[0][3]
	entry_results = {"url":"","published":""}
	try: # entry.feedburner_origlink:
		url = entry.feedburner_origlink
	except:
		url = entry.link
	try:# entry.published_parsed:
		published = entry.published_parsed
	except:
		pass
	entry_results = {"url":url,"published":published}
	return entry_results




# from scrapers.embed_scraper import *
# from scrapers.models import *
# results = scrape_all([factmag])
# track = results["tracks"][0]
# source = track["source"]
# url = track["url"]
# original_slug = track["title"]
# s = Source(url = source)
# s.save()
# sound = Sound(original_slug = original_slug)
# sound.save()



def save_track(track):
	source_name = track.pop("source")
	url = track.pop("url")
	original_slug = track.pop("title")
	date_published = track.pop("published")
	if len(Source.objects.filter(url=source)) > 0:
		source_entry = Source.objects.get(url=source)
	else:
		source_entry = Source(url = url)
		source_entry.save()
	track_entry = Sound(original_slug = original_slug)




	for k,v in track.items():
		track_entry.k = v
	track_entry.save()
	track_entry.source = source_entry
	track_entry.save()
	post = Post(source = source, post_url = url, sound = track_entry)
	post.save()

def save_playlist(playlist):
	pass



YT_playlist = "8BCDD04DE8F771B2"
YT_track = "vIELl2tgblg"
SC_playlist = "639839"
SC_track = "82195284"
vimeo_track = "48425421"

def check_for_embeds(url):
	YT = []
	SC = []	
	vimeo = []
	soup = make_soup(url)
	SC = find_soundcloud(soup)
	YT = find_youtube(soup)
	vimeo = find_vimeo(soup)
	if len(YT) > 0 and len(SC) > 0 and len(vimeo) > 0:
		return True
	else:
		return False


def check_lastfm(slug):
	slug = slug.encode("utf8")
	slug = urllib2.quote(slug) 
	url = "http://ws.audioscrobbler.com/2.0/?method=track.search&track="+slug+"&api_key="+last_fm_api_key+"&format=json"
	data = urllib2.urlopen(url)
	data = json.load(data)
	return data

def extract(slug):
	slug = slug.encode("utf8")
	slug = urllib2.quote(slug)
	url = "http://developer.echonest.com/api/v4/artist/extract?api_key="+echo_nest_API_key+"&format=json&text="+slug+"&results=10"
	data = urllib2.urlopen(url)
	data = json.load(data)
	return data

soup = make_soup(url)
scrape(url)




# <iframe width="100%" height="166" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=http%3A%2F%2Fapi.soundcloud.com%2Ftracks%2F82195284"></iframe>


# <iframe width="100%" height="450" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=http%3A%2F%2Fapi.soundcloud.com%2Fplaylists%2F639839"></iframe>


# https://w.soundcloud.com/player/?url=http%3A%2F%2Fapi.soundcloud.com%2Fplaylists%2F4681384%3Fsecret_token%3Ds-NZVkr
# <iframe width="100%" height="166" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=http%3A%2F%2Fapi.soundcloud.com%2Ftracks%2F87172296&secret_token=s-NZVkr"></iframe>

# <embed id="video-player" height="100%" width="100%" tabindex="0" type="application/x-shockwave-flash" src="http://s.ytimg.com/yts/swfbin/watch_as3-vfl5qlEPI.swf" allowscriptaccess="always" bgcolor="#000000" allowfullscreen="true" flashvars="list=PLIOK0_bYXe1qcB3QATgC5pwAZccRXbFZq&amp;sendtmp=1&amp;is_html5_mobile_device=false&amp;playlist_module=http%3A%2F%2Fs.ytimg.com%2Fyts%2Fswfbin%2Fplaylist_module-vflzGeMnk.swf&amp;eurl=http%3A%2F%2Fsheblogsaboutmusic.wordpress.com%2F2013%2F02%2F28%2Fctm-saul-yum%2F&amp;probably_logged_in=1&amp;rel=1&amp;length_seconds=95&amp;enablejsapi=1&amp;iurl=http%3A%2F%2Fi3.ytimg.com%2Fvi%2FJp6KpQBUaNw%2Fhqdefault.jpg&amp;video_id=Jp6KpQBUaNw&amp;el=embedded&amp;allow_ratings=1&amp;title=CTM%20-%20Variations&amp;hl=en_US&amp;avg_rating=5&amp;share_icons=http%3A%2F%2Fs.ytimg.com%2Fyts%2Fswfbin%2Fsharing-vflsBOuhL.swf&amp;iurlsd=http%3A%2F%2Fi3.ytimg.com%2Fvi%2FJp6KpQBUaNw%2Fsddefault.jpg&amp;playlist_length=3&amp;user_display_name=santiagoangel10&amp;playlist_title=CTM&amp;user_display_image=https%3A%2F%2Fs.ytimg.com%2Fyts%2Fimg%2Fsilhouette32-vflu0yzhs.png&amp;cr=AU&amp;fexp=930900%2C932000%2C932004%2C906383%2C916910%2C902000%2C901208%2C919512%2C929903%2C925714%2C931202%2C900821%2C900823%2C931203%2C906090%2C909419%2C908529%2C930807%2C919373%2C930803%2C906836%2C920201%2C929602%2C930101%2C926403%2C900824%2C910223&amp;allow_embed=1&amp;view_count=4277&amp;sk=KzzRcNBG6ZLCHZCupVWHRJPBXx1FEoYMC&amp;jsapicallback=ytPlayerOnYouTubePlayerReady&amp;playerapiid=player1&amp;framer=http%3A%2F%2Fsheblogsaboutmusic.wordpress.com%2F2013%2F02%2F28%2Fctm-saul-yum%2F">


# def showNext(i, scripts):
# 	i = i
# 	i+=1
# 	return scripts[i]


# for entry in xlr8r.entries:
# 	try:
# 		print scrape(entry.link)
# 	except urllib2.HTTPError as e:
# 		print e

# def scrape_feed(RSSfeeds):
# 	results = []
# 	for site in RSSfeeds:
# 		feed = feedparser.parse(site)
# 		source = feed.feed.link
# 		for entry in feed.entries:
# 			rss_data = get_RSS_json(entry)
# 			rss_data["source"] = source
# 			track_results = scrape(rss_data["url"])
# 			for entry in track_results["tracks"]:
# 				track_results.update(rss_data)
# 			for entry in track_results["playlists"]:
# 				track_results.update(rss_data)
# 			results.append(track_results)
# 	return results

# def scrape(url):
# 	YT = []
# 	SC = []	
# 	vimeo = []
# 	soup = make_soup(url)
# 	SC = find_soundcloud(soup)
# 	YT = find_youtube(soup)
# 	vimeo = find_vimeo(soup)
# 	SCresults = []
# 	YTresults = []
# 	Vresults = []
# 	results = []
# 	for track in vimeo:
# 		if track["type"] == "track":
# 			data = get_vimeo_track(track["link"])
# 			Vresults.append(data)
# 	for track in SC:
# 		if track["type"] == "playlist":
# 			data = get_SC_playlist(track["link"])
# 			SCresults.append(data)
# 		if track["type"] == "track":
# 			data = get_SC_track(track["link"])
# 			SCresults.append(data)
# 	for track in YT:
# 		if track["type"] == "playlist":
# 			data = get_YT_playlist(track["link"])
# 			YTresults.append(data)
# 		if track["type"] == "track":
# 			data = get_YT_track(track["link"])
# 			YTresults.append(data)
# 	results.append({"Vimeo Tracks":Vresults})
# 	results.append({"SC Tracks":SCresults})
# 	results.append({"YT Tracks":YTresults})
# 	return results
	
