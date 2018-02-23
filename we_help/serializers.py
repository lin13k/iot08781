from rest_framework import serializers
from .models import Event, SignUp


class EventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    create_time = serializers.TimeField(read_only=True)
    update_time = serializers.TimeField(read_only=True)

    class Meta:
        model = Event
        fields = (
            'create_by', 'content', 'close_time',
            'event_time', 'create_time', 'update_time'
        )


class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    create_time = serializers.TimeField(read_only=True)
    update_time = serializers.TimeField(read_only=True)

    class Meta:
        model = SignUp
        fields = ('id', 'event', 'profile', 'is_pick_up',
                  'create_time', 'update_time')
