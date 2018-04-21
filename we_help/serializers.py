from rest_framework import serializers
from .models import Event, SignUp, Message
from accounts.serializers import UserSerializer
from django.contrib.auth.models import User


class EventSerializerWithoutSignups(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(read_only=True)
    create_user = serializers.PrimaryKeyRelatedField(
        required=False, queryset=User.objects.all())

    class Meta:
        model = Event
        fields = ('id', 'title', 'description',
                  'create_user', 'close_time',
                  'create_time', 'duration', 'reward',
                  'longitude', 'latitude', 'address', 'place',
                  )


class EventSerializerWithoutSignupsForRead(EventSerializerWithoutSignups):
    create_user = UserSerializer()


class SignUpSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)
    id = serializers.ModelField(
        model_field=SignUp()._meta.get_field('id'), required=False)

    class Meta:
        model = SignUp
        fields = ('id', 'event', 'signup_user', 'is_pick_up',
                  'create_time', 'update_time')


class SignUpSerializerForRead(SignUpSerializer):
    signup_user = UserSerializer()


class EventSerializerWithSignups(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)
    signups = SignUpSerializer(many=True)

    class Meta:
        model = Event
        fields = ('id', 'signups',
                  'create_user', 'content', 'close_time',
                  'create_time', 'update_time', 'duration',
                  'longitude', 'latitude', 'address', 'place',
                  )

    def update(self, instance, validated_data):
        signupsData = validated_data.pop('signups', None)
        super().update(instance, validated_data)
        print(signupsData)
        for signup in signupsData:
            if 'id' in signup:
                signupModel = SignUp.objects.get(id=signup['id'])
                signupModel.is_pick_up = signup['is_pick_up']
                signupModel.save()
        return instance


class EventSerializerWithSignupsForRead(EventSerializerWithSignups):
    create_user = UserSerializer()
    signups = SignUpSerializerForRead(
        many=True)


class MessageSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver',
                  'content', 'create_time',)
