from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from .forms import PropertyForm
from .models import Property, Reservation
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
    return JsonResponse(serializer.data, safe=False)

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

@api_view(['POST'])
def book_property(request, pk):
    """
    Book a property.
    """
    try:
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        number_of_nights = request.POST.get('number_of_nights', '')
        total_price = request.POST.get('total_price', '')
        guests = request.POST.get('guests', '')
        
        property = Property.objects.get(pk=pk)
        Reservation.objects.create(
            property=property,
            start_date=start_date,
            end_date=end_date,
            number_of_nights=number_of_nights,
            total_price=total_price,
            guests=guests,
            created_by=request.user
        )
            
    except Exception as e:
        print('error', e)
        return JsonResponse({'error': 'Could not create reservation'}, status=400)
    
    
    # property = Property.objects.get(pk=pk)
    # start_date = request.data.get('start_date')
    # end_date = request.data.get('end_date')
    # guests = request.data.get('guests')

    # # Calculate number of nights
    # from datetime import datetime
    # start = datetime.strptime(start_date, '%Y-%m-%d')
    # end = datetime.strptime(end_date, '%Y-%m-%d')
    # number_of_nights = (end - start).days

    # total_price = number_of_nights * property.price

    # from .models import Reservation
    # reservation = Reservation.objects.create(
    #     property=property,
    #     start_date=start_date,
    #     end_date=end_date,
    #     number_of_nights=number_of_nights,
    #     guests=guests,
    #     total_price=total_price,
    #     created_by=request.user
    # )

    return JsonResponse({'success': True, 'reservation_id': str(reservation.id)})