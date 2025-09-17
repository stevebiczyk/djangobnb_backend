from django.urls import path
from . import api

urlpatterns = [
    path('', api.properties_list, name='api_properties-list'),
    path('create/', api.create_property, name='api_create_property'),
]