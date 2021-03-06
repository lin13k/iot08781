from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from we_help import serializers
from we_help.models import Event, SignUp
from django.shortcuts import get_object_or_404, HttpResponse
from rest_framework.response import Response
from mimetypes import guess_type
from rest_framework import permissions
from django.db.models import Q


class NearByEventViewSet(ModelViewSet):
    queryset = Event.objects.all()

    def get_serializer_class(self):
        print('get serializer_class', self.action)
        if self.action == 'list':
            return serializers.EventSerializerWithoutSignupsForRead
        else:
            return serializers.EventSerializerWithoutSignups

    def list(self, request):
        print(request.GET)
        if 'longitude' not in request.GET or 'latitude' not in request.GET:
            return Response({'error':
                             'You must provide longitude and latitude.'}, 400)

        longitude = float(request.GET['longitude'])
        latitude = float(request.GET['latitude'])

        self.queryset = Event.objects.near(
            latitude, longitude, 10).filter(
            status=Event.OPEN).exclude(
            create_user=request.user).exclude(
            signups__signup_user=request.user
        )

        return super().list(request)

    def create(self, request):
        eventData = dict(request.data)
        eventData['create_user'] = request.user.id
        s = self.get_serializer_class()(data=eventData)
        if not s.is_valid():
            return Response({'error': s.errors}, 400)
        s.save()
        return Response(s.data)


class CreatedEventViewSet(ModelViewSet):
    serializer_class = serializers.EventSerializerWithSignups

    def get_serializer_class(self):
        print('get serializer_class', self.action)
        if self.action in ('list', 'retrieve'):
            return serializers.EventSerializerWithSignupsForRead
        else:
            return serializers.EventSerializerWithSignups

    def get_queryset(self):
        return Event.objects.filter(
            ~Q(status=Event.CLOSED),
            create_user=self.request.user,
        )


class SignedEventViewSet(ModelViewSet):
    serializer_class = serializers.EventSerializerWithoutSignupsForRead

    def get_queryset(self):
        return Event.objects.filter(
            Q(signups__signup_user=self.request.user),
            ~Q(status=Event.CLOSED),
        )


class SignupEventView(APIView):
    # serializer_class = serializers.SignUpSerializer

    # def get_serializer_class(self):
    #     if self.action == ':
    #         pass

    def get(self, request, pk):
        return Response({'error': 'Use post method to sign up event'})

    def post(self, request, pk):
        event = get_object_or_404(Event, id=pk)
        if event.create_user == request.user:
            return Response(
                {'error': 'You cannot sign up your own event'}, 400)
        if event in Event.objects.filter(
                Q(signups__signup_user=self.request.user)):
            return Response({'error': 'You already signed up this event'}, 400)
        signup = SignUp.objects.create(event=event, signup_user=request.user)
        return Response(serializers.SignUpSerializerForRead(signup).data)

    def delete(self, request, pk):
        event = get_object_or_404(Event, id=pk)
        signedEvents = Event.objects.filter(
            Q(signups__signup_user=self.request.user))
        if event not in signedEvents:
            return Response(
                {'error': 'You do not sign up this event yet'}, 400)
        SignUp.objects.filter(event=event, signup_user=request.user).delete()
        return Response({'message': 'delete the signup successfully'}, 200)


class EventPhotoView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, id):
        event = get_object_or_404(
            Event, id=id)

        # Probably don't need this check as form
        # validation requires a picture be uploaded.
        if not event.pic:
            try:
                with open('images/default.png', "rb") as f:
                    return HttpResponse(f.read(), content_type="image/png")
            except IOError:
                response = HttpResponse(IOError.strerror, 400)
                return response

        return HttpResponse(event.pic, content_type=guess_type(
            event.pic.name.split('/')[-1]
        ))
