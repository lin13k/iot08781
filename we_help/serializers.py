from rest_framework import serializers
from .models import Event, SignUp, Message
from accounts.serializers import UserSerializer
from django.contrib.auth.models import User
from drf_extra_fields.fields import Base64ImageField


class EventSerializerWithoutSignups(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(read_only=True)
    create_user = serializers.PrimaryKeyRelatedField(
        required=False, queryset=User.objects.all())
    pic = Base64ImageField(required=False)
    is_pick_up = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id', 'title', 'description',
                  'create_user', 'close_time',
                  'create_time', 'duration', 'reward',
                  'longitude', 'latitude', 'address', 'place',
                  'status', 'pic', 'is_pick_up',
                  )

    def get_is_pick_up(self, obj):
        return True if obj.signups.filter(
            signup_user=self.context['request'].user,
            is_pick_up=True,
        ).exists() else False


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


class EventSerializerWithSignups(EventSerializerWithoutSignups):
    create_time = serializers.DateTimeField(read_only=True)
    signups = SignUpSerializer(many=True)
    pic = Base64ImageField(required=False)

    class Meta:
        model = Event
        fields = ('id', 'title', 'description',
                  'create_user', 'close_time',
                  'create_time', 'duration', 'reward',
                  'longitude', 'latitude', 'address', 'place',
                  'status', 'signups',
                  'pic',
                  )

    def update(self, instance, validated_data):
        signupsData = validated_data.pop('signups', None)
        super().update(instance, validated_data)
        print(signupsData)
        if not signupsData:
            return instance
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
