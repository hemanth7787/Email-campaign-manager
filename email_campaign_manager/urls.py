from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^ecm/', include('ecm_core.urls')),
    url(r'^login/', 'ecm_core.views.login', name='login'),
    url(r'^logout/', 'ecm_core.views.logout', name='logout'),
    url(r'^$', 'ecm_core.views.home', name='home'),

)
