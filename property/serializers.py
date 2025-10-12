from rest_framework import serializers

from .models import Property

from accounts.serializers import UserDetailSerializer

class PropertiesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = (
            'id',
            'title',
            'price',
            'image_url',
        )
        
class PropertiesDetailSerializer(serializers.ModelSerializer):
    landlord = UserDetailSerializer(read_only=True, many=False)
    class Meta:
        model = Property
        fields = (
            'id',
            'title',
            'description',
            'price',
            'bedrooms',
            'bathrooms',
            'guests',
            'category',
            'image_url',
            'landlord',
        )