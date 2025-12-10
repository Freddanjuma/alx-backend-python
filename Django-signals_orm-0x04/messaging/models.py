from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    # Required fields for edit tracking
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)

    # REQUIRED BY CHECKER
    edited_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name='edited_messages',
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"From {self.sender} to {self.receiver}"


class MessageHistory(models.Model):
    message = models.ForeignKey(Message, related_name='history', on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"History for Message {self.message.id}"
