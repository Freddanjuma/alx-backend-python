# messaging/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

# import the custom manager
from .managers import UnreadMessagesManager

User = get_user_model()

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)

    edited_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name='edited_messages',
        on_delete=models.SET_NULL
    )

    parent_message = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    # new boolean field for read/unread status (if not already present)
    read = models.BooleanField(default=False)

    # Default manager
    objects = models.Manager()
    # Custom unread manager exposed as "unread"
    unread = UnreadMessagesManager()

    def __str__(self):
        return f"From {self.sender} to {self.receiver}"

    def get_direct_replies(self):
        return self.replies.all().select_related("sender", "receiver")

    def get_all_thread_replies(self):
        thread = []
        def collect(msg):
            for reply in msg.replies.all().select_related("sender", "receiver"):
                thread.append(reply)
                collect(reply)
        collect(self)
        return thread
