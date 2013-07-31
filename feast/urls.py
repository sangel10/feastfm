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
    url(r'^artist/(?P<artist_id>[^/]+)/$', 'scrapers.views.artist_browse'),
    url(r'^label/(?P<label_id>[^/]+)/$', 'scrapers.views.label'),
    url(r'^search/$', 'scrapers.views.search'),
    url(r'^lastfm_search/$', 'scrapers.views.lastfm_search'),
    url(r'^follow_toggle/$', 'scrapers.views.follow_toggle'),
    url(r'^stream/$', 'scrapers.views.stream'),
    url(r'^soundcloud_search/$', 'scrapers.views.soundcloud_search'),
    #url(r'^login/$', 'django.contrib.auth.views.login'),
    #url(r'^accounts/', include('registration.urls')),
    url(r'^accounts/register/$',
		CustomRegistrationView.as_view(),
    	name='registration_register',
    	),
    url(r'^accounts/', include('registration.backends.simple.urls')),

    # url(r'^feast/', include('feast.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
