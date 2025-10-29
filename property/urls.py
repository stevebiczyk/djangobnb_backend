from django.urls import path
from . import api

urlpatterns = [
    path('', api.properties_list, name='api_properties_list'),
    path('create/', api.create_property, name='api_create_property'),
    path('<uuid:pk>/', api.properties_detail, name='api_properties_detail'),
    path('<uuid:pk>/booking/', api.book_property, name='api_book_property'),
    path('reservations/mine/', api.my_reservations, name='my_reservations'),
    path('<uuid:pk>/reservations/', api.property_reservations, name='api_property_reservations'),
]