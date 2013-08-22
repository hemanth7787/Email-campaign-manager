from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^open/$', 'ecm_track.views.open_track', name='track'),
    )