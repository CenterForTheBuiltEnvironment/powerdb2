
from django.conf.urls import *

urlpatterns = patterns('',
    (r'^.*$', 'backend.views.proxy')
)
