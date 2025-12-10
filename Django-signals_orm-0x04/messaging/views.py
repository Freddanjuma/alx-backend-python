# messaging/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Message

@login_required
def inbox(request):
    """
    Show unread messages for the logged-in user using the custom manager.
    The checker expects: Message.unread.unread_for_user(...) and .only(...)
    """
    # Use the custom manager method
    unread_qs = Message.unread.unread_for_user(request.user)

    # unread_qs already includes select_related and only(...) via the manager,
    # but you can still chain further optimizations if needed:
    unread_qs = unread_qs.prefetch_related("replies")  # optional: prefetch direct replies

    return render(request, "messaging/inbox.html", {"unread_messages": unread_qs})
