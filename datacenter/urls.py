
from django.conf.urls import *

urlpatterns = patterns('',
    (r'^$', 'powerdb2.datacenter.views.status'),
)
