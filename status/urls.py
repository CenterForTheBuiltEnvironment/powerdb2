
from django.conf.urls import *

urlpatterns = patterns('',
    (r'^$', 'status.views.status'),
)
