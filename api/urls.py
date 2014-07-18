
from django.conf.urls import *
from piston.resource import Resource
from api.handlers import SubscriptionHandler

subscription_handler = Resource(SubscriptionHandler)

urlpatterns = patterns('',
   (r'^subscriptions/(?P<backend_id>[0-9]+)', subscription_handler),
   (r'^subscriptions/', subscription_handler),
  )
