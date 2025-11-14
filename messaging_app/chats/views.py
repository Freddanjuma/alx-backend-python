from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["participants__username"]

    def create(self, request, *args, **kwargs):
        """Create a new conversation"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["conversation__id", "sender__username"]

    def create(self, request, *args, **kwargs):
        """Send message to an existing conversation"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        conversation_id = request.data.get("conversation")
        conversation = get_object_or_404(Conversation, id=conversation_id)

        message = serializer.save(conversation=conversation)

        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
