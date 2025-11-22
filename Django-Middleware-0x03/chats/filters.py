import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    """
    Filter for messages:
    - 'user': filter by sender's username or email
    - 'date': filter messages sent after a specific date
    """
    user = django_filters.CharFilter(field_name='sender__username', lookup_expr='icontains')
    date = django_filters.DateFilter(field_name='sent_at', lookup_expr='gte') # Greater Than or Equal

    class Meta:
        model = Message
        fields = ['user', 'date', 'conversation']
