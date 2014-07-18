
from django.conf.urls import *

urlpatterns = patterns('',
    (r'^$', 'powerdb2.status.views.status'),
)
