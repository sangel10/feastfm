from django.db import models

# Create your models here.

# if SC playlist is posted, DJ set = true, and then each song is 
# DJ sets are considered sounds
class Sound(models.Model):
	title = models.CharField(max_length = 500, blank=True)

	# already have many to many relation for these
	#sources = models.ManyToManyField(Source, related_name = 'sounds')
	#artist = models.ManyToManyField(Artist)
	#post = posts
	#labels = labels

	original_slug = models.CharField(max_length = 500)

	yt_track_id = models.CharField(max_length = 500, blank=True, unique=True)
	sc_track_id = models.CharField(max_length = 500, blank=True, unique=True)
	vimeo_track_id = models.CharField(max_length = 500, blank=True, unique=True)

	sc_username = models.CharField(max_length = 500, blank=True)
	sc_full_name = models.CharField(max_length = 500, blank=True)
	vimeo_username = models.CharField(max_length = 500, blank=True)

	sc_release = models.CharField(max_length = 500, blank=True)
	sc_label = models.CharField(max_length = 500, blank=True)

	#when scraping mixesDB
	first_appeared = models.DateTimeField(blank=True, null = True)
	DJ_set = models.BooleanField(blank=True)
	tracklist_models = models.ManyToManyField('self', blank=True) #used for searching relationships
	tracklist = models.TextField(blank=True) # used for rendering tracklists, bc list can be ordered
	original_tracklist = models.TextField(blank=True) # as a reference, in the event we want to go back and reparse text
	mix_series = models.CharField(max_length = 1000, blank = True) # default = false
	mix_series_number = models.IntegerField(blank=True, null=True)

	discogs_id = models.CharField(max_length = 500, blank=True)
	release_number = models.CharField(max_length = 500, blank=True)
	length = models.IntegerField(blank=True, null = True)
	sound_duplicates = models.ManyToManyField('self', blank=True)

	def __unicode__(self):
		return self.original_slug


class Source(models.Model):
	url = models.TextField(blank=True, unique=True)
	name = models.CharField(max_length = 500)
	sounds = models.ManyToManyField(Sound, related_name = "source")
	
	def __unicode__(self):
		return self.url
	def __repr__(self):
		return self.url

# you could have a playlist of DJ Sets, 
# dj sets are considered sounds, 
#collections of soudns are considered playlists
class Playlist(models.Model):
	name = models.TextField(blank=True)
	sc_playlist_id = models.CharField(max_length = 500, blank=True, unique = True)
	yt_playlist_id = models.CharField(max_length = 500, blank=True, unique = True)
	vimeo_playlist_id = models.CharField(max_length = 500, blank=True, unique = True)
	sounds = models.ManyToManyField(Sound, related_name = 'playlists')
	tracklist = models.TextField() # used for rendering tracklists, bc list can be ordered

	def __unicode__(self):
		return self.name



class Post(models.Model):
	post_url = models.TextField(unique = True)
	source = models.ForeignKey(Source, related_name = 'posts') #mixesDB, discogsDUMP, specific website
	playlist = models.ManyToManyField(Playlist, related_name = 'posts', blank=True) # default = False, #many to many bc can have multiple playlists/songs in post
	sound = models.ManyToManyField(Sound, related_name = 'posts', blank=True)
	date_posted = models.DateTimeField(blank=True, null=True)

	# def __unicode__(self):
	# 	return self.id

class Label(models.Model):
	name = models.CharField(max_length = 500)
	label_duplicates = models.ManyToManyField('self', blank=True)

	#artists = models.ManyToManyField(Artist)
	sounds = models.ManyToManyField(Sound, related_name = 'labels')
	sources = models.ManyToManyField(Source, related_name= 'labels')
	posts = models.ManyToManyField(Post, related_name = 'labels')

	def __unicode__(self):
		return self.name

class Artist(models.Model):
	name = models.CharField(max_length = 500)
	artist_duplicates = models.ManyToManyField('self', blank=True)

	labels = models.ManyToManyField(Label, related_name = 'artists', blank=True)
	sounds = models.ManyToManyField(Sound, related_name = 'artists', blank=True)
	sources = models.ManyToManyField(Source, related_name = 'artists', blank=True)
	posts = models.ManyToManyField(Post, related_name = 'artists', blank=True)

	def __unicode__(self):
		return self.name










