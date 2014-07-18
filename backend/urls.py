
from django.conf.urls import *

urlpatterns = patterns('',
    (r'^.*$', 'powerdb2.backend.views.proxy')
)
