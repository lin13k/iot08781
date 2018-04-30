from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework_jwt.views import ObtainJSONWebToken
from django.shortcuts import get_object_or_404, HttpResponse
from rest_framework import permissions
from accounts.serializers import *
from django.contrib.auth.models import User
from mimetypes import guess_type
from .models import Profile
from django.db import transaction


class UserCreate(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    @transaction.atomic
    def post(self, request, format='json'):
        # userData = dict(request.data)
        # profileData = userData.pop('profile')
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Profile.objects.create(user=user)
            if user:
                tokenView = ObtainJSONWebToken()
                tokenView.request = request
                return tokenView.post(request, format='json')
        return Response({'errors': serializer.errors}, 400)


class PublicProfileViewSet(ModelViewSet):
    serializer_class = PublicProfileSerializer
    queryset = Profile.objects.all()


class PrivateProfileViewSet(ModelViewSet):
    serializer_class = PrivateProfileSerializer
    queryset = Profile.objects.all()


class PrivateProfileView(APIView):
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    serializer_class = PrivateProfileSerializer

    def get(self, request):
        pk = Profile.objects.filter(user=request.user)[0].pk
        view = PrivateProfileViewSet.as_view({
            'get': 'retrieve'
        })
        return view(request, pk=pk, action='retrieve')

    def put(self, request):
        pk = Profile.objects.filter(user=request.user)[0].pk
        view = PrivateProfileViewSet.as_view({
            'put': 'update'
        })
        return view(request, pk=pk, action='update')


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
                response = HttpResponse(IOError.strerror, 400)
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
                response = HttpResponse(IOError.strerror, 400)
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
