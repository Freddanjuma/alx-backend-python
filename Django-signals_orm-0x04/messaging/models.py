from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


# Custom Manager for unread messages
class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """
        Return unread messages for a specific user.
        Optimized with .only() to fetch only necessary fields.
        """
        return (
            super()
            .get_queryset()
            .filter(receiver=user, read=False)
            .select_related("sender", "receiver")
            .only("id", "sender", "receiver", "content", "timestamp")
        )


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    # Edit tracking from previous tasks
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)

    edited_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name='edited_messages',
        on_delete=models.SET_NULL
    )

    # Threading (from prior task)
    parent_message = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies"
    )

    # NEW FIELD: read/unread status
    read = models.BooleanField(default=False)

    # Default Manager
    objects = models.Manager()

    # Custom unread manager
    unread = UnreadMessagesManager()

    def __str__(self):
        return f"From {self.sender} to {self.receiver}"

    def get_direct_replies(self):
        return self.replies.all().select_related("sender", "receiver")

    # Recursive threaded replies
    def get_all_thread_replies(self):
        thread = []

        def collect(msg):
            for reply in msg.replies.all().select_related("sender", "receiver"):
                thread.append(reply)
                collect(reply)

        collect(self)
        return thread
