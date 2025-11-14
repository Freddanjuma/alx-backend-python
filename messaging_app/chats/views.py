from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

User = get_user_model()


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def get_queryset(self):
        """
        Only return conversations where the authenticated user is a participant.
        """
        user = self.request.user
        return Conversation.objects.filter(participants=user)

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with a list of participants.
        Expected payload:
        {
            "participants": ["user_id_1", "user_id_2"]
        }
        """
        participants = request.data.get("participants", [])

        if not participants:
            return Response({"error": "Participants field is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Ensure users exist
        users = User.objects.filter(id__in=participants)

        if users.count() != len(participants):
            return Response({"error": "One or more user IDs are invalid"},
                            status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        conversation.participants.set(users)
        conversation.save()

        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and sending messages in a conversation.
    """
    serializer_class = MessageSerializer

    def get_queryset(self):
        conversation_id = self.kwargs.get("conversation_pk")
        return Message.objects.filter(conversation__conversation_id=conversation_id)

    def create(self, request, *args, **kwargs):
        """
        Create a message in an existing conversation.
        Expected payload:
        {
            "message_body": "Hello there!"
        }
        """
        conversation_id = self.kwargs.get("conversation_pk")
        
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found"},
                            status=status.HTTP_404_NOT_FOUND)

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            message_body=request.data.get("message_body")
        )

        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
