from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory


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
