from django.db.models.signals import pre_save
from .models import Message, MessageHistory
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    """
    Automatically deletes all user-related data when a User account is deleted.
    This includes:
    - messages authored by the user
    - notifications belonging to the user
    - message edit histories associated with the user
    """
    Message.objects.filter(user=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(user=instance).delete()

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Detect changes in message content before saving.
    If content changed, log the old content and mark message as edited.
    """
    if not instance.pk:
        return  # message is new, do nothing

    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # Check if content changed
    if old_message.content != instance.content:
        # Mark as edited
        instance.edited = True

        # Save history
        MessageHistory.objects.create(
            message=instance,
            old_content=old_message.content
        )
