from rest_framework import serializers
from .models import Event, SignUp, Message


class EventSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Event
        fields = (
            'create_user', 'content', 'close_time',
            'create_time', 'update_time', 'duration',
            'longitude', 'latitude', 'address', 'place',
        )


class SignUpSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SignUp
        fields = ('event', 'signup_user', 'is_pick_up',
                  'create_time', 'update_time')


class MessageSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Message
        fields = ('sender', 'receiver',
                  'content', 'create_time',)
