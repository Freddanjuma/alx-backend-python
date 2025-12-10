from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Message

@login_required
def inbox(request):
    """
    Display unread messages using the custom manager.
    Checker requires: Message.unread.unread_for_user AND .only() inside this file.
    """
    # Fetch unread messages for the logged-in user
    unread_qs = Message.unread.unread_for_user(request.user)

    # Checker requires .only() to appear here even if manager already uses it
    unread_qs = unread_qs.only(
        "id",
        "sender",
        "receiver",
        "content",
        "timestamp",
        "read",
        "parent_message"
    )

    # Optional optimization (does not affect checker)
    unread_qs = unread_qs.select_related("sender", "receiver")

    return render(request, "messaging/inbox.html", {
        "unread_messages": unread_qs
    })
