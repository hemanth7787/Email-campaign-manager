from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
   url(r'^contacts/$', 'ecm_core.views.contacts', name='contacts'),
   url(r'^contacts-view/$', 'ecm_core.views.contacts_view', name='contacts_view'),
   url(r'^contacts-search/$', 'ecm_core.views.contacts_search', name='contacts_search'),
   url(r'^import/$', 'ecm_core.views.import_csv', name='import_csv'),
   url(r'^statistics/$', 'ecm_core.views.contacts_statistics', name='contacts_statistics'),

   url(r'^campaign/unsubscribe/(?P<usid>[\w-]+)/$', 'ecm_core.views.unsubscribe', name='unsubscribe'),
   #----------------------------

   url(r'^campaign/$', 'ecm_core.views.campaign', name='campaign'),
   url(r'^view-campaign/$', 'ecm_core.views.view_campaign', name='view_campaign'),
   url(r'^run-campaign/$', 'ecm_core.views.run_campaign', name='run_campaign'),
   url(r'^campaign-report/$', 'ecm_core.views.campaign_report', name='report'),


   url(r'^getreport/$', 'ecm_core.views.json_report', name='get_json_report'),

   url(r'^templates/$', 'ecm_core.views.templates', name='templates'),
   url(r'^templates-new/$', 'ecm_core.views.templates_new', name='templates_new'),
   url(r'^templates-view/$', 'ecm_core.views.templates_view', name='templates_view'),
   url(r'^templates-preview/(?P<usid>[\w-]+)/$', 'ecm_core.views.templates_preview', name='templates_preview'),
   url(r'^templates-delete/(?P<usid>[\w-]+)/$', 'ecm_core.views.templates_delete', name='templates_delete'),

   url(r'^dummy/login_redirect$', 'ecm_core.views.dummy_login_redirect', name='dummy_login_redirect'),

)

