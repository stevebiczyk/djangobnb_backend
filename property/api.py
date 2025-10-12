from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from .forms import PropertyForm
from .models import Property
from .serializers import PropertiesListSerializer, PropertiesDetailSerializer

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_list(request):
    """
    List all properties.
    """
    properties = Property.objects.all()
    serializer = PropertiesListSerializer(properties, many=True)
    return JsonResponse(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_detail(request, pk):
    """
    Retrieve a property by ID.
    """
    property = Property.objects.get(pk=pk)
    
    serializer = PropertiesDetailSerializer(property, many=False)
    return JsonResponse({'data':serializer.data})
    # except Property.DoesNotExist:
    #     return JsonResponse({'error': 'Property not found'}, status=404)

    # serializer = PropertiesListSerializer(property)
    # return JsonResponse({'data':serializer.data})

@api_view(['POST', 'FILES'])
def create_property(request):
    """
    Create a new property.
    """
    form = PropertyForm(request.POST, request.FILES)
    if form.is_valid():
        property = form.save(commit=False)
        property.landlord = request.user
        property.save()

        return JsonResponse({'succes': True})
    else:
        print('error', form.errors, form.non_field_errors)
    return JsonResponse({'errors':form.errors.as_json()}, status=400)