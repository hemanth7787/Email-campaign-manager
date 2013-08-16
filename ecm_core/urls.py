from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
   
   url(r'^campaign/unsubscribe/(?P<usid>[\w-]+)/', 'ecm_core.views.unsubscribe', name='unsubscribe'),

   url(r'^campaign/', 'ecm_core.views.campaign', name='campaign'),
   url(r'^run-campaign/', 'ecm_core.views.run_campaign', name='run_campaign'),
   url(r'^report/', 'ecm_core.views.campaign_report', name='report'),

   url(r'^test/', 'ecm_core.views.test', name='test'),

   url(r'^contacts/', 'ecm_core.views.contacts', name='contacts'),
   url(r'^contacts-view/', 'ecm_core.views.contacts_view', name='contacts_view'),
   url(r'^import/', 'ecm_core.views.import_csv', name='import_csv'),
   url(r'^statistics/', 'ecm_core.views.contacts_statistics', name='contacts_statistics'),

   url(r'^templates/', 'ecm_core.views.templates', name='templates'),


   url(r'^/', 'ecm_core.views.home', name='home'),

)
