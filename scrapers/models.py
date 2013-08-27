from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

# if SC playlist is posted, DJ set = true, and then each song is 
# DJ sets are considered sounds
class Sound(models.Model):
	original_slug = models.CharField(max_length = 500)
	title = models.CharField(max_length = 500, blank=True)

	yt_track_id = models.CharField(max_length = 500, blank=True)
	sc_track_id = models.CharField(max_length = 500, blank=True)
	vimeo_track_id = models.CharField(max_length = 500, blank=True)
	mbid = models.CharField(max_length = 500, blank=True)
	scraped = models.BooleanField(default = False)

	sc_username = models.CharField(max_length = 500, blank=True)
	sc_full_name = models.CharField(max_length = 500, blank=True)
	vimeo_username = models.CharField(max_length = 500, blank=True)

	length = models.IntegerField(blank=True, null = True)
	sound_duplicates = models.ManyToManyField('self', blank=True, null=True)

	def __unicode__(self):
		if self.original_slug:
			return self.original_slug
		# elif self.artists:
		# 	return self.artists
		else:
			return self.title
	# def __repr__(self):
	# 	return self.original_slug




class Source(models.Model):
	url = models.TextField(blank=True, unique=True, )
	name = models.CharField(max_length = 500)
	sounds = models.ManyToManyField(Sound, related_name = "source", null=True)
	
	def __unicode__(self):
		return self.url
	# def __repr__(self):
	# 	return self.url

# you could have a playlist of DJ Sets, 
# dj sets are considered sounds, 
#collections of soudns are considered playlists
class Playlist(models.Model):
	name = models.TextField(blank=True)
	sc_playlist_id = models.CharField(max_length = 500, blank=True)
	yt_playlist_id = models.CharField(max_length = 500, blank=True)
	vimeo_playlist_id = models.CharField(max_length = 500, blank=True)
	sounds = models.ManyToManyField(Sound, related_name = 'playlists', null=True)

	def __unicode__(self):
		return self.name



class Post(models.Model):
	post_url = models.TextField()
	source = models.ForeignKey(Source, related_name = 'posts', null=True) #mixesDB, discogsDUMP, specific website
	playlist = models.ManyToManyField(Playlist, related_name = 'posts', blank=True, null=True) # default = False, #many to many bc can have multiple playlists/songs in post
	sound = models.ManyToManyField(Sound, related_name = 'posts', blank=True, null=True)
	date_posted = models.DateTimeField(blank=True, null=True)

	def __unicode__(self):
		return self.post_url

class Label(models.Model):
	name = models.CharField(max_length = 500)
	label_duplicates = models.ManyToManyField('self', blank=True, null=True)
	mbid = models.CharField(max_length = 500, blank=True)

	sounds = models.ManyToManyField(Sound, related_name = 'labels', null=True)
	sources = models.ManyToManyField(Source, related_name= 'labels', null=True)
	posts = models.ManyToManyField(Post, related_name = 'labels', null=True)

	def __unicode__(self):
		return self.name

class Artist(models.Model):
	name = models.CharField(max_length = 500)
	artist_duplicates = models.ManyToManyField('self', blank=True, null=True)
	mbid = models.CharField(max_length = 500, blank=True)

	labels = models.ManyToManyField(Label, related_name = 'artists', blank=True, null=True)
	sounds = models.ManyToManyField(Sound, related_name = 'artists', blank=True, null=True)
	sources = models.ManyToManyField(Source, related_name = 'artists', blank=True, null=True)
	posts = models.ManyToManyField(Post, related_name = 'artists', blank=True, null=True)

	def __unicode__(self):
		return self.name


class mbz_release(models.Model):
	mbz_reid = models.CharField(max_length = 500)
	mbz_catalog_number = models.CharField(max_length = 500)


class Release_group(models.Model):
	mbz_rgid= models.CharField(max_length = 500)
	artists = models.ManyToManyField(Artist, related_name = 'release_groups', blank=True, null=True)
	labels = models.ManyToManyField(Label, related_name = 'release_groups', blank=True, null=True)
	sounds = models.ManyToManyField(Sound, related_name = 'release_groups', blank=True, null=True)
	sources = models.ManyToManyField(Source, related_name = 'release_groups', blank=True, null=True)
	mbz_releases = models.ManyToManyField(mbz_release, related_name = 'release_groups', blank=True, null=True)
	date_released = models.DateTimeField(blank=True, null=True)


class MixesDB_mix(models.Model):
	artists = models.ManyToManyField(Artist, related_name = 'mixes', blank=True, null=True)
	labels = models.ManyToManyField(Label, related_name = 'mixes', blank=True, null=True)
	original_slug = models.CharField(max_length = 500)
	title = models.CharField(max_length = 500, blank=True)
	length = models.IntegerField(blank=True, null = True)
	mix_duplicates = models.ManyToManyField('self', blank=True, null=True)
	sounds = models.ManyToManyField(Sound, related_name = 'mixes', blank=True, null=True)

	def __unicode__(self):
		return self.title

class Mix_Series(models.Model):
	name = models.CharField(max_length = 500)
	mixes = models.ManyToManyField(MixesDB_mix, related_name = "mix series", blank=True, null = True)

	def __unicode__(self):
		return self.name


class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)
    artists = models.ManyToManyField(Artist, related_name = "users", blank=True, null = True)
    labels = models.ManyToManyField(Label, related_name = "users", blank=True, null = True)
    sources = models.ManyToManyField(Source, related_name = "users", blank=True, null = True)
    mix_series = models.ManyToManyField(Mix_Series, related_name = "users", blank=True, null = True)
    sounds = models.ManyToManyField(Sound, related_name = "users", blank=True, null = True)

  #   def __unicode__(self):
		# return self.user

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


