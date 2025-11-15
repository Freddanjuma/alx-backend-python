from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Include chats app API routes under /api/
    path('api/', include('chats.urls')),
]
