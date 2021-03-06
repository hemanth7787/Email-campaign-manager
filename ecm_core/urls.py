from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
   url(r'^contacts/$', 'ecm_core.views.contacts', name='contacts'),
   url(r'^contacts-view/$', 'ecm_core.views.contacts_view', name='contacts_view'),
   url(r'^contacts-search/$', 'ecm_core.views.contacts_search', name='contacts_search'),
   url(r'^contacts-delete/$', 'ecm_core.views.contacts_delete', name='contacts_delete'),
   url(r'^contacts-add/$', 'ecm_core.views.add_contact', name='contacts_add'),
   url(r'^contacts-edit/(?P<cid>\d+)/$', 'ecm_core.views.edit_contact', name='contacts_edit'),
   url(r'^contacts-details/(?P<cid>\d+)/$', 'ecm_core.views.contacts_details', name='contacts_details'),
   url(r'^contacts-history/(?P<cid>\d+)/$', 'ecm_core.views.contacts_history', name='contacts_history'),

   url(r'^maillist-export/(?P<data_type>[\w-]+)/(?P<id>\d+)/$', 'ecm_core.views.maillist_export', name='maillist_export'),
   url(r'^maillist-delete/$', 'ecm_core.views.maillist_delete', name='maillist_delete'),
   url(r'^import/$', 'ecm_core.views.import_csv', name='import_csv'),
   url(r'^statistics/$', 'ecm_core.views.contacts_statistics', name='contacts_statistics'),

   url(r'^campaign/unsubscribe/(?P<usid>[\w-]+)/$', 'ecm_core.views.unsubscribe', name='unsubscribe'),
   #----------------------------

   url(r'^campaign/$', 'ecm_core.views.campaign', name='campaign'),
   url(r'^view-campaign/$', 'ecm_core.views.view_campaign', name='view_campaign'),
   url(r'^run-campaign/$', 'ecm_core.views.run_campaign', name='run_campaign'),
   url(r'^campaign-report/$', 'ecm_core.views.campaign_report', name='report'),

   url(r'^drafts/$', 'ecm_core.views.camp_drafts', name='draft'),
   url(r'^sent-drafts/(?P<camp_id>\d+)/$', 'ecm_core.views.camp_drafts_sent', name='draft-sent'),
   url(r'^drafts-delete/(?P<camp_id>\d+)/$', 'ecm_core.views.camp_drafts_delete', name='draft-delete'),
   url(r'^draft-edit/(?P<camp_id>\d+)/$', 'ecm_core.views.camp_drafts_edit', name='draft-edit'),


   url(r'^getreport/$', 'ecm_core.views.json_report', name='get_json_report'),

   url(r'^templates/$', 'ecm_core.views.templates', name='templates'),
   url(r'^templates-new/$', 'ecm_core.views.templates_new', name='templates_new'),
   url(r'^templates-view/$', 'ecm_core.views.templates_view', name='templates_view'),
   url(r'^templates-preview/(?P<usid>[\w-]+)/$', 'ecm_core.views.templates_preview', name='templates_preview'),
   url(r'^templates-delete/(?P<usid>[\w-]+)/$', 'ecm_core.views.templates_delete', name='templates_delete'),

   url(r'^dummy/login_redirect$', 'ecm_core.views.dummy_login_redirect', name='dummy_login_redirect'),

)

