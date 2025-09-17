from django.forms import ModelForm
from property.models import Property

class PropertyForm(ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'price', 'bedrooms', 'bathrooms', 'guests', 'country', 'country_code', 'category', 'image']