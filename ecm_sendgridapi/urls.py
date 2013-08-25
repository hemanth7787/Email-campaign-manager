from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^blocks/$', 'ecm_sendgridapi.views.sendgrid_blocks', name='extra_blocks'),
    url(r'^bounces/$', 'ecm_sendgridapi.views.sendgrid_bounces', name='extra_bounces'),
    url(r'^unsubscribes/$', 'ecm_sendgridapi.views.sendgrid_unsubscribes', name='extra_unsubscribes'),
    url(r'^spam-reports/$', 'ecm_sendgridapi.views.sendgrid_spamreports', name='extra_spamreports'),
    )

