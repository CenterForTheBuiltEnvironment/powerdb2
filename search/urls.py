
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^getresultsStatus/', 'search.views.getresultsStatus'),
    (r'^genQuery/', 'search.views.genQuery'),
    (r'^getNextSearchResults/', 'search.views.getNextSearchResults'),
    (r'^getExtraResults/', 'search.views.getExtraResults'), 
    (r'^replace/', 'search.views.replace'), 
    (r'^getMetadata/', 'search.views.getMetadata'),
    (r'^getSimilar/', 'search.views.getSimilar'),
    (r'^updateMetadata/', 'search.views.updateMetadata'),
    (r'^getresults/', 'search.views.getresults'),
    (r'^$', 'search.views.search'),
)
