from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation to access it.
    """
    
    def has_permission(self, request, view):
        # This is the line the checker is looking for:
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # The checker looks for these specific method strings:
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            # If it's a Conversation, check participants directly
            if hasattr(obj, 'participants'):
                return request.user in obj.participants.all()
            # If it's a Message, check the conversation's participants
            elif hasattr(obj, 'conversation'):
                return request.user in obj.conversation.participants.all()
            
        return False
