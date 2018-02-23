from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from accounts.serializers import UserSerializer, ProfileSerializer
from django.contrib.auth.models import User
from .models import Profile


class UserCreate(APIView):
    """ 
    Creates the user. 
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            Profile.objects.create(user=user)
            if user:
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)


class ProfileViewSet(ModelViewSet):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user
        return Profile.objects.filter(user=user)

    def retrieve(self, request, pk=None):
        profile = get_object_or_404(self.get_queryset(), pk=pk)
        print(profile, profile.user, profile.pic, profile.pic_id)
        return Response({
            'user_id': profile.user, 'pic': profile.pic if profile.pic else '',
            'pic_id': profile.pic_id if profile.pic_id else ''})