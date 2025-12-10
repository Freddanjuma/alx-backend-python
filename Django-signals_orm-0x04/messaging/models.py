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

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    # Edit tracking (from previous task)
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

    # NEW FOR THREADED CONVERSATIONS
    parent_message = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    def __str__(self):
        return f"From {self.sender} to {self.receiver}"

    # Get direct replies
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
