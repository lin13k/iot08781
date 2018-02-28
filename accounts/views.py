from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework_jwt.views import ObtainJSONWebToken
from django.shortcuts import get_object_or_404, HttpResponse
from rest_framework import status, permissions
from accounts.serializers import UserSerializer, ProfileSerializer
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from mimetypes import guess_type
from .models import Profile


class UserCreate(ObtainJSONWebToken):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            Profile.objects.create(user=user)
            if user:
                return super(UserCreate, self).post(request, format='json')
        return Response({'errors': serializer.errors})


class ProfileViewSet(ModelViewSet):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user
        return Profile.objects.filter(user=user)

    def retrieve(self, request, pk=None):
        profile = get_object_or_404(self.get_queryset(), pk=pk)
        print(profile, profile.user, profile.pic, profile.pic_id)
        return Response({
            'user_id': profile.user.id,
            'pic': str(profile.pic) if profile.pic else '',
            'pic_id': str(profile.pic_id) if profile.pic_id else ''})

    def update(self, request, pk=None):
        print('update profile')
        super(ProfileViewSet, self).update(request, pk=pk)
        return self.retrieve(request, pk=pk)


class ProfilePhotoView(APIView):

    def get(self, request, id):
        profile = get_object_or_404(
            Profile, user=User.objects.get(id=id))

        # Probably don't need this check as form
        # validation requires a picture be uploaded.
        if not profile.pic:
            try:
                with open('images/default.png', "rb") as f:
                    return HttpResponse(f.read(), content_type="image/png")
            except IOError:
                response = HttpResponse(IOError.strerror)
                return response

        return HttpResponse(profile.pic, content_type=guess_type(
            profile.pic.name.split('/')[-1]
        ))


class ProfileIDPhotoView(APIView):

    def get(self, request):
        profile = get_object_or_404(
            Profile, user=request.user)

        # Probably don't need this check as form
        # validation requires a picture be uploaded.
        if not profile.pic_id:
            try:
                with open('images/default.png', "rb") as f:
                    return HttpResponse(f.read(), content_type="image/png")
            except IOError:
                response = HttpResponse(IOError.strerror)
                return response

        return HttpResponse(profile.pic_id, content_type=guess_type(
            profile.pic_id.name.split('/')[-1]
        ))


# @login_required
# def ProfilePhotoView(request, id):
#     profile = get_object_or_404(
#         Profile, user=User.objects.get(id=id))

#     # Probably don't need this check as form
#     # validation requires a picture be uploaded.
#     if not profile.pic:
#         try:
#             with open('images/default.png', "rb") as f:
#                 return HttpResponse(f.read(), content_type="image/png")
#         except IOError:
#             response = HttpResponse(IOError.strerror)
#             return response

#     return HttpResponse(profile.pic, content_type=guess_type(
#         profile.pic.name.split('/')[-1]
#     ))
