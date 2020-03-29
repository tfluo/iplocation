
from django.conf.urls import url

from api.views.location import get_location, get_location_entity

urlpatterns = [
        url('^$', get_location),
        url('', get_location_entity),
]
