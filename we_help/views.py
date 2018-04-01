from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from we_help import serializers
from we_help.models import Event
from rest_framework.exceptions import APIException
from rest_framework.response import Response
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
            return Response(
                'You must provide longitude and latitude.', 400)

        longitude = float(request.GET['longitude'])
        latitude = float(request.GET['latitude'])

        self.queryset = Event.objects.near(latitude, longitude, 10)
        return super().list(request)


class CreatedEventViewSet(ModelViewSet):
    serializer_class = serializers.EventSerializerWithSignups

    def get_serializer_class(self):
        print('get serializer_class', self.action)
        if self.action in ('list', 'retrieve'):
            return serializers.EventSerializerWithSignupsForRead
        else:
            return serializers.EventSerializerWithSignups

    def get_queryset(self):
        return Event.objects.filter(create_user=self.request.user)


class SignedEventViewSet(ModelViewSet):
    serializer_class = serializers.EventSerializerWithoutSignups

    def get_queryset(self):
        return Event.objects.filter(Q(signups__signup_user=self.request.user))


class SignupEventView(APIView):
    serializer_class = serializers.SignUpSerializerForRead

    # def get_serializer_class(self):
    #     if self.action == ':
    #         pass

    # def get(self, request, pk):
    #     return Response('Use post method to sign up event')

    # def post(self, request, pk):
        
