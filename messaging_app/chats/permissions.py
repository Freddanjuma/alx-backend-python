
from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation to access it.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users to access the API
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        'obj' is the specific Conversation or Message instance being accessed.
        """
        # If the object is a Conversation, check if user is a participant
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        
        # If the object is a Message, check if user is a participant of the conversation
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        return False
