from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from djcelery.models import (TaskState, WorkerState,PeriodicTask, IntervalSchedule, CrontabSchedule)

admin.site.unregister(TaskState)
admin.site.unregister(WorkerState)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(PeriodicTask)

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^ecm/', include('ecm_core.urls')),
    url(r'^fruits/', include('ecm_track.urls')),
    url(r'^analytics/', include('ecm_sendgridapi.urls')),
    url(r'^login/$', 'ecm_core.views.login', name='login'),
    url(r'^logout/$', 'ecm_core.views.logout', name='logout'),
    url(r'^$', 'ecm_core.views.home', name='home'),
    url(r'^about', 'ecm_core.views.dummy', name='dummy'),
    url(r'^ckeditor/', include('ckeditor.urls')),

)


# DEBUGing: Static file serve for DEBUG puposes
from django.conf import settings
if settings.DEBUG:
    # For user-uploaded media
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            'show_indexes': True,
        }),
    )
    # For static media
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
