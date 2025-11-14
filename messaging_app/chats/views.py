from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from django.db.models import Q
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer, 
    MessageSerializer, 
    MessageCreateSerializer
)

class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows conversations to be viewed or created.
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should only return conversations
        that the current user is a participant in.
        """
        user = self.request.user
        # 'conversations' is the related_name from the User model
        return user.conversations.all()

    def perform_create(self, serializer):
        """
        When creating a new conversation, automatically add
        the current user as a participant.
        """
        # We save the conversation, which returns the instance
        conversation = serializer.save()
        # 'participants' is a ManyToMany field, so we use .add()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or sent.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should only return messages from conversations
        that the current user is a participant in.
        """
        user = self.request.user
        # We filter messages where the conversation has the user as a participant
        return Message.objects.filter(conversation__participants=user)

    def get_serializer_class(self):
        """
        Use a different serializer for 'create' (sending a message)
        vs. 'list' or 'retrieve' (reading messages).
        """
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer

    def perform_create(self, serializer):
        """
        When sending a new message, automatically set
        the 'sender' to the currently logged-in user.
        """
        # We pass the sender (the current user) to the serializer's create method
        serializer.save(sender=self.request.user)
