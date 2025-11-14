from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message

# Get the custom User model we defined
User = get_user_model()


# --- 1. User Serializer ---
# This serializer is basic and will be nested in the others.
# We only include fields that are safe to show publicly.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'role')


# --- 2. Message Serializer ---
# This will be nested inside the ConversationSerializer.
# We want to show the sender's details, not just their ID.
class MessageSerializer(serializers.ModelSerializer):
    # This nests the UserSerializer inside this one
    sender = UserSerializer(read_only=True) 

    class Meta:
        model = Message
        # We explicitly list the fields we want to show
        fields = ('id', 'sender', 'message_body', 'sent_at')


# --- 3. Conversation Serializer ---
# This is the main serializer that fulfills all requirements.
# It nests both the participants and the messages.
class ConversationSerializer(serializers.ModelSerializer):
    
    # Requirement 1: Handle ManyToMany (participants)
    # This nests the UserSerializer (many=True) to show a list of all participants.
    participants = UserSerializer(many=True, read_only=True)
    
    # Requirement 2: Handle nested relationships (messages)
    # This nests the MessageSerializer (many=True) to show all messages
    # 'messages' is the 'related_name' we set on the Message model.
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ('id', 'participants', 'created_at', 'messages')
