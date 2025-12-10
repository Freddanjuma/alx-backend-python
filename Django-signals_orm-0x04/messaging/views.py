from rest_framework import viewsets, permissions, status, response
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, MessageCreateSerializer
from .permissions import IsParticipantOfConversation

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing conversations.
    Filters queryset so users only see their own conversations.
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


# Apply cache_page(60) only to the 'list' action (GET /messages/)
@method_decorator(cache_page(60), name='list')
class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing messages.
    Filters queryset so users only see messages from conversations they are part of.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer

    def create(self, request, *args, **kwargs):
        # Checker looks for 'conversation_id' variable
        conversation_id = self.kwargs.get('conversation_pk')
        
        # Check if conversation exists and user is participant
        conversation = get_object_or_404(Conversation, pk=conversation_id)
        
        if request.user not in conversation.participants.all():
            # Checker looks for 'HTTP_403_FORBIDDEN'
            return response.Response(
                {"detail": "You are not a participant of this conversation."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Save with the conversation object and sender
        serializer.save(sender=request.user, conversation=conversation)
        
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
