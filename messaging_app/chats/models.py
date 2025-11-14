import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# --- 1. User Model ---
# Based on the schema: User(user_id, first_name, last_name, email, etc.)
# Extends AbstractUser as per instructions.

class User(AbstractUser):
    """
    Custom User model extending AbstractUser.
    
    Uses email as the unique identifier and adds a UUID primary key,
    phone number, and user role as per the schema.
    """

    # --- Define ENUM choices for Role ---
    class Role(models.TextChoices):
        GUEST = 'guest', _('Guest')
        HOST = 'host', _('Host')
        ADMIN = 'admin', _('Admin')

    # --- Override fields from AbstractUser ---
    
    # Disable the 'username' field, as per schema (email is login)
    username = None

    # Schema: user_id (Primary Key, UUID, Indexed)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,  # Matches schema "Indexed"
        verbose_name=_("User ID")
    )

    # Schema: email (VARCHAR, UNIQUE, NOT NULL)
    email = models.EmailField(
        _('email address'),
        unique=True,      # Matches schema "UNIQUE"
        blank=False,      # Matches schema "NOT NULL"
        null=False        # Matches schema "NOT NULL"
    )

    # Schema: first_name (VARCHAR, NOT NULL)
    first_name = models.CharField(
        _('first name'), 
        max_length=150, 
        blank=False,      # Matches schema "NOT NULL"
        null=False        # Matches schema "NOT NULL"
    )
    
    # Schema: last_name (VARCHAR, NOT NULL)
    last_name = models.CharField(
        _('last name'), 
        max_length=150, 
        blank=False,      # Matches schema "NOT NULL"
        null=False        # Matches schema "NOT NULL"
    )

    # --- Add new fields from the schema ---

    # Schema: phone_number (VARCHAR, NULL)
    phone_number = models.CharField(
        _('phone number'),
        max_length=20,
        null=True,        # Matches schema "NULL"
        blank=True
    )

    # Schema: role (ENUM: 'guest', 'host', 'admin', NOT NULL)
    role = models.CharField(
        _('role'),
        max_length=10,
        choices=Role.choices,
        default=Role.GUEST,
        blank=False,      # Matches schema "NOT NULL"
        null=False        # Matches schema "NOT NULL"
    )

    # --- Set the login field ---
    USERNAME_FIELD = 'email'
    
    # --- Set required fields for 'createsuperuser' command ---
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # Note: 'created_at' is handled by 'date_joined' field from AbstractUser.
    # Note: 'password_hash' is handled by 'password' field from AbstractUser.

    def __str__(self):
        return self.email

# --- 2. Conversation Model ---
# Based on the schema: Conversation(conversation_id, participants_id, created_at)

class Conversation(models.Model):
    """
    Model for a conversation, linking multiple participants.
    """
    # Schema: conversation_id (Primary Key, UUID, Indexed)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
        verbose_name=_("Conversation ID")
    )
    
    # Schema: participants_id (Foreign Key, references User(user_id))
    # Implemented as a ManyToManyField to allow multiple users,
    # which is required for a group chat.
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,  # This safely points to 'chats.User'
        related_name='conversations'
    )
    
    # Schema: created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
    created_at = models.DateTimeField(
        auto_now_add=True,  # Automatically sets to now on creation
        verbose_name=_("Created At")
    )

    def __str__(self):
        return f"Conversation ({self.id})"

# --- 3. Message Model ---
# Based on the schema: Message(message_id, sender_id, message_body, sent_at)
# Also includes 'conversation' as per the main task instruction.

class Message(models.Model):
    """
    Model for an individual message within a conversation.
    """
    # Schema: message_id (Primary Key, UUID, Indexed)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
        verbose_name=_("Message ID")
    )

    # INSTRUCTION: "containing the sender, conversation..."
    # This field links the message to its conversation.
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,  # If a conversation is deleted, delete its messages
        related_name='messages'
    )
    
    # Schema: sender_id (Foreign Key, references User(user_id))
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,  # If user is deleted, keep message, set sender to NULL
        null=True,
        related_name='sent_messages'
    )
    
    # Schema: message_body (TEXT, NOT NULL)
    message_body = models.TextField(
        blank=False,  # Matches schema "NOT NULL"
        null=False    # Matches schema "NOT NULL"
    )
    
    # Schema: sent_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
    sent_at = models.DateTimeField(
        auto_now_add=True,  # Automatically sets to now on creation
        verbose_name=_("Sent At")
    )

    def __str__(self):
        return f"Message from {self.sender} at {self.sent_at}"
    
    class Meta:
        # Ensures messages are ordered by when they were sent
        ordering = ['sent_at']
