from rest_framework import serializers
from .models import ScheduledEvent

class ScheduledEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledEvent
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'user']