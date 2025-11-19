from rest_framework import viewsets, permissions, status, response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing conversations.
    Filters queryset so users only see their own conversations.
    """
    serializer_class = ConversationSerializer
    # Apply the custom permission. 
    # Note: IsParticipantOfConversation already checks for authentication in our implementation.
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        # Ensure users only see conversations they participate in
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        # Create conversation and automatically add the current user as a participant
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing messages.
    Filters queryset so users only see messages from conversations they are part of.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        # Ensure users only see messages from their conversations
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the sender to the current user
        serializer.save(sender=self.request.user)
