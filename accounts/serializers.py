from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile
from drf_extra_fields.fields import Base64ImageField


class UserCreateProfileSerializer(serializers.ModelSerializer):
    pic = Base64ImageField(required=False)
    pic_id = Base64ImageField(required=False)

    class Meta:
        model = Profile
        fields = ('pic', 'pic_id', 'phone')


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8, write_only=True)
    profile = UserCreateProfileSerializer(required=False)

    def create(self, validated_data):
        profileData = validated_data.pop('profile')
        user = User.objects.create_user(
            validated_data['username'], validated_data['email'],
            validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'])
        Profile.objects.create(user=user, **profileData)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'password', 'first_name', 'last_name', 'profile')


class PublicProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    pic_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'pic_url', 'phone')

    def get_pic_url(self, obj):
        return self.context['request'].build_absolute_uri(
            reverse('photo', args=[obj.user.id]))


class PrivateProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    pic_url = serializers.SerializerMethodField(read_only=True)
    pic_id_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'pic', 'pic_id', 'pic_url', 'pic_id_url', 'phone')

    def get_pic_url(self, obj):
        return self.context['request'].build_absolute_uri(
            reverse('photo', args=[obj.user.id]))

    def get_pic_id_url(self, obj):
        return self.context['request'].build_absolute_uri(
            reverse('id-photo'))
