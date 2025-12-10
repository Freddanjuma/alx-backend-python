# messaging/managers.py
from django.db import models

class UnreadMessagesManager(models.Manager):
    """
    Custom manager that returns unread messages for a given user.
    Exposes unread_for_user(user) which returns a queryset optimized with
    select_related and only(...) to load minimal necessary fields.
    """
    def unread_for_user(self, user):
        # Return unread messages where the given user is the receiver
        return (
            super()
            .get_queryset()
            .filter(receiver=user, read=False)
            .select_related("sender", "receiver", "parent_message")
            .only("id", "sender", "receiver", "content", "timestamp", "parent_message")
            .order_by("-timestamp")
        )
