from django.conf.urls import patterns, include, url
from registration.backends.simple.views import RegistrationView
from scrapers.views import CustomRegistrationView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'scrapers.views.home'),
    url(r'^album_ajax/$', 'scrapers.views.get_album_tracks'),
    url(r'^lastfm_album_tracks/$', 'scrapers.views.get_album_tracks_lastfm'), 
    url(r'^artist/(?P<artist_id>[^/]+)/$', 'scrapers.views.artist_browse'),
    url(r'^artist_name/(?P<artist>[^/]+)/$', 'scrapers.views.artist_by_name'),
    url(r'^label/(?P<label_id>[^/]+)/$', 'scrapers.views.label'),
   
    # url(r'^search/$', 'scrapers.views.search'),
    url(r'^search/$', 'scrapers.views.full_search'),
    url(r'^advanced_search/$', 'scrapers.views.import_artists'),
    url(r'^lastfm_search/$', 'scrapers.views.lastfm_search'),
    url(r'^follow_toggle/$', 'scrapers.views.follow_toggle'),
    url(r'^follow_album/$', 'scrapers.views.follow_album'),
    url(r'^stream/$', 'scrapers.views.stream'),
    url(r'^soundcloud_search/$', 'scrapers.views.soundcloud_search'),
    url(r'^my_follows/$', 'scrapers.views.my_follows'),
    url(r'^my_sounds/$', 'scrapers.views.my_sounds'),
    url(r'^all_sounds/$', 'scrapers.views.all_sounds'),
    url(r'^create_playlist/$', 'scrapers.views.create_playlist'),
    url(r'^get_playlists/$', 'scrapers.views.get_playlists'),
    url(r'^my_playlists/$', 'scrapers.views.my_playlists'),
    url(r'^album_to_playlist/$', 'scrapers.views.add_album_to_playlist'),
    url(r'^track_to_playlist/$', 'scrapers.views.add_track_to_playlist'),
    url(r'^playlist/(?P<playlist_id>[^/]+)/$', 'scrapers.views.playlist_view'),
    url(r'^source/(?P<source_id>[^/]+)/$', 'scrapers.views.songs_by_source'),



    #url(r'^login/$', 'django.contrib.auth.views.login'),
    #url(r'^accounts/', include('registration.urls')),
    url(r'^accounts/register/$',
		CustomRegistrationView.as_view(),
    	name='registration_register',
    	),
    # url(r'^accounts/', include('registration.backends.simple.urls')),

    url(r'^accounts/', include('registration.urls')),

    # url(r'^feast/', include('feast.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
