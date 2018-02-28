from rest_framework import serializers
from .models import Event, SignUp, Message


class EventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    create_time = serializers.TimeField(read_only=True)
    update_time = serializers.TimeField(read_only=True)

    class Meta:
        model = Event
        fields = (
            'create_user', 'content', 'close_time',
            'event_time', 'create_time', 'update_time',
            'longitude', 'latitude', 'address',
        )


class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    create_time = serializers.TimeField(read_only=True)
    update_time = serializers.TimeField(read_only=True)

    class Meta:
        model = SignUp
        fields = ('id', 'event', 'signup_user', 'is_pick_up',
                  'create_time', 'update_time')


class MessageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    create_time = serializers.TimeField(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver',
                  'content', 'create_time',)
