from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Conversation
from .serializers import ConversationListSerializer

@api_view(["GET"])
def conversations_list(request):
    serializer = ConversationListSerializer(request.user.conversations.all(), many=True)
    
    return Response(serializer.data)
