from rest_framework.viewsets import ModelViewSet
from we_help.serializers import EventSerializer
from we_help.models import Event
from rest_framework.exceptions import APIException
from rest_framework.response import Response


class EventView(ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def list(self, request):
        print(request.GET)
        if 'longitude' not in request.GET or 'latitude' not in request.GET:
            return Response(
                'You must provide longitude and latitude.', 400)

        longitude = float(request.GET['longitude'])
        latitude = float(request.GET['latitude'])

        queryset = Event.objects.near(latitude, longitude, 10)
        serializer = EventSerializer(queryset, many=True)

        return Response(serializer.data)
