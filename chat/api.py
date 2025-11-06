from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Conversation
from .serializers import ConversationListSerializer, ConversationDetailSerializer

@api_view(["GET"])
def conversations_list(request):
    serializer = ConversationListSerializer(request.user.conversations.all(), many=True)
    
    return Response(serializer.data)

@api_view(["GET"])
def conversations_detail(request, pk):
    conversation = request.user.conversations.filter(pk=pk)
    
    conversations_serializer = ConversationDetailSerializer(conversation, many=False)
    
    return Response(conversations_serializer.data)