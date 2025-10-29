from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import uuid

from .forms import PropertyForm
from .models import Property, Reservation
from .serializers import PropertiesListSerializer, PropertiesDetailSerializer, ReservationsListSerializer

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_list(request):

    properties = Property.objects.all()
    
    # ✅ Expect a single landlord_id, not a list
    landlord_id = request.GET.get('landlord_id')
    if landlord_id:
        # Optional: validate it’s a UUID so you return 400 not 500 on bad input
        try:
            uuid.UUID(landlord_id)
        except ValueError:
            return JsonResponse(
                {"detail": "Invalid landlord_id"},
                status=400
            )
        properties = properties.filter(landlord_id=landlord_id)

    # Serialize the properties
    data = PropertiesListSerializer(properties, many=True).data

    # If you also want to return favorite IDs for the current user:
    # Adjust this block to your actual favorites model/relationship.
    favorite_ids = []
    # Example if you have a ManyToMany on Property like favorited = models.ManyToManyField(User, ...)
    # and you only want favorites among the returned queryset:
    if request.user.is_authenticated and hasattr(Property, "favorited"):
        favorite_ids = list(
            properties.filter(favorited=request.user).values_list("id", flat=True)
        )

    # ✅ Return the shape your frontend expects
    return JsonResponse(
        {"data": data, "favorites": favorite_ids},
        safe=False
    )
    # #
    # # Filter by landlord ID if provided
    
    # landlord_id = request.GET.get('landlord_id', '')
    # if landlord_id:
    #     properties = properties.filter(landlord__id__in=landlord_id)
        
    # #
    # # Favorite filtering
    # user = getattr(request, 'user', None)
    # print('User', user)
    # if user and getattr(user, 'is_authenticated', False):
    #     for prop in properties:
    #         if user in prop.favorited.all():
    #             favorites.append(prop.id)

    
    # #
    # # Serialize and return the data
    # serializer = PropertiesListSerializer(properties, many=True)
    # return JsonResponse(serializer.data,favorites, safe=False)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_detail(request, pk):
    """
    Retrieve a property by ID.
    """
    property = Property.objects.get(pk=pk)
    
    serializer = PropertiesDetailSerializer(property, many=False)
    return JsonResponse(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def property_reservations(request, pk):
    """
    List reservations for a specific property.
    """
    property = Property.objects.get(pk=pk)
    reservations = property.reservations.all()
    
    serializer = ReservationsListSerializer(reservations, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_reservations(request):
    """
    List my reservations.
    """
    qs = (
        Reservation.objects
        .filter(created_by=request.user)
        .select_related("property")
        .order_by("-created_at")
    )
    serializer = ReservationsListSerializer(qs, many=True, context={"request": request})
    return Response(serializer.data)

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
            
        return JsonResponse({'success': True})
    except Exception as e:
        print('Error', e)

        return JsonResponse({'success': False})
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_favorite(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    user = request.user

    if prop.favorited.filter(pk=user.pk).exists():
        prop.favorited.remove(user)
        is_favorite = False
    else:
        prop.favorited.add(user)
        is_favorite = True

    return Response({"id": str(prop.id), "is_favorite": is_favorite})
    
# @api_view(['POST'])
# def toggle_favorite(request, pk):
#     """
#     Toggle favorite status for a property.
#     """
#     property = Property.objects.get(pk=pk)
    
#     if request.user in property.favorited.all():
#         property.favorited.remove(request.user)
#         return JsonResponse({'is_favorite': False})
#     else:
#         property.favorited.add(request.user)
#         return JsonResponse({'is_favorite': True})
    