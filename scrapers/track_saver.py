

from scrapers.embed_scraper import *
from scrapers.models import *
from time import mktime
from datetime import datetime


results = scrape_all([factmag])
track = results["tracks"][0]

def save_track(track):
	track_type = track["type"]
	source_url = track["source"]
	post_url = track["url"]
	original_slug = track["title"]
	length = track["length"]
	date = track["published"]
	date = datetime.fromtimestamp(mktime(date))
	if Source.objects.filter(url=source_url):
		source = Source.objects.filter(url=source_url)[0]
	else:
		source = Source(url = source_url)
		source.save()
	if Post.objects.filter(post_url = post_url, date_posted = date):
		post = Post.objects.filter(post_url=post_url)[0]
	else:
		post = Post(post_url = post_url, date_posted = date)
		post.save()
	if track_type == "sc":
		sc_track_id = track["sc_track_id"]
		if Sound.objects.filter(sc_track_id = sc_track_id):
			sound = Sound.objects.filter(sc_track_id = sc_track_id)[0]
		else:
			sound = Sound(sc_track_id = sc_track_id, original_slug = original_slug, sc_username = track["sc_username"], sc_full_name = track["sc_full_name"])
			sound.save()
	if track_type == "yt":
		yt_track_id = track["yt_track_id"]
		if Sound.objects.filter(yt_track_id = yt_track_id):
			sound = Sound.objects.filter(yt_track_id = yt_track_id)[0]
		else:
			sound = Sound(yt_track_id = yt_track_id, original_slug = original_slug)
			sound.save()
	if track_type == "vimeo":
		vimeo_track_id = track["vimeo_track_id"]
		if Sound.objects.filter(vimeo_track_id = vimeo_track_id):
			sound = Sound.objects.filter(vimeo_track_id = vimeo_track_id)[0]
		else:
			sound = Sound(vimeo_track_id = vimeo_track_id, original_slug = original_slug, vimeo_username = track["vimeo_username"])
			sound.save()
	# for k in track:
	# 	sound.k = track[k]
	sound.save()
	sound.posts.add(post)
	sound.source.add(source)
	sound.save()
	source.posts.add(post)
	source.save()
	return source,post,sound


