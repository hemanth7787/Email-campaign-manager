from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
   url(r'^import/', 'ecm_core.views.Import_csv', name='import_csv'),
   url(r'^campaign/unsubscribe/(?P<usid>[\w-]+)/', 'ecm_core.views.unsubscribe', name='unsubscribe'),
   url(r'^campaign/', 'ecm_core.views.campain', name='campaign'),

)
