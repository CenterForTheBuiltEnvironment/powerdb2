from django.conf.urls import *
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^powerdb/', include('powerdb.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^plot/', include('smap2.urls')),

    (r'^status/', include('status.urls')),

    (r'^backend/', include('backend.urls')),

    (r'^backend_auth/', include('backend.urls')),

                       # (r'^api/', include('powerdb2.api.urls')),

#    (r'^datacenter/', include('powerdb2.datacenter.urls')),

    (r'^robots.txt.*', 'views.robots'),

    # (r'^alert/', include('alert.urls')),

    (r'^$', 'views.root'),
     
    (r'^status/', include('status.urls')),
    
    (r'^dashboard/', 'status.views.dashboard'),

    (r'^smap_query/', 'status.views.smap_query')
)

urlpatterns += staticfiles_urlpatterns()
