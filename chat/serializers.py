from rest_framework import serializers
from .models import Conversation, Message
from accounts.serializers import UserDetailSerializer

class ConversationListSerializer(serializers.ModelSerializer):
    participants = UserDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at', 'modified_at']
        
class ConversationDetailSerializer(serializers.ModelSerializer):
    participants = UserDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at', 'modified_at']