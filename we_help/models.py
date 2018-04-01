from django.db import models
from geopy import units, distance
from geopy.geocoders.googlev3 import GeocoderQueryError
from geopy import geocoders
from django.conf import settings


# Create your models here.


class GeoManager(models.Manager):
    def near(self, latitude=None, longitude=None, distance_range=30):
        queryset = super(GeoManager, self).get_queryset()

        if not (latitude and longitude and distance_range):
            return queryset.none()

        latitude = float(latitude)
        longitude = float(longitude)
        distance_range = float(distance_range)

        rough_distance = units.degrees(
            arcminutes=units.nautical(kilometers=distance_range)) * 2

        queryset = queryset.filter(
            latitude__range=(
                latitude - rough_distance,
                latitude + rough_distance
            ),
            longitude__range=(
                longitude - rough_distance,
                longitude + rough_distance
            )
        )

        locations = []
        for location in queryset:
            if location.latitude and location.longitude:
                exact_distance = distance.distance(
                    (latitude, longitude),
                    (location.latitude, location.longitude)
                ).kilometers

                if exact_distance <= distance_range:
                    locations.append(location)

        queryset = queryset.filter(id__in=[l.id for l in locations])
        return queryset


class BaseGeo(models.Model):
    address = models.TextField(blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    place = models.TextField(blank=True)
    objects = GeoManager()

    class Meta:
        abstract = True

    def save(self, domain='maps.google.com.my', *args, **kwargs):
        address = self.address
        print('in BaseGeo save')
        if address:
            if not self.latitude or not self.longitude:
                try:
                    g = geocoders.GoogleV3(
                        api_key=settings.GOOGLE_API_KEY)
                    self.place, (self.latitude,
                                 self.longitude) = g.geocode(address)
                except GeocoderQueryError:
                    print(GeocoderQueryError.args)
                except Exception as e:
                    print('%s' % e)

        super(BaseGeo, self).save(*args, **kwargs)


class Event(BaseGeo):
    create_user = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name='events')
    content = models.TextField(max_length=500)
    close_time = models.DateTimeField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    duration = models.IntegerField(default=0)


class EventImage(models.Model):
    file = models.FileField(upload_to='images/event')
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='images')


class SignUp(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='signups')
    signup_user = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name='signups')
    is_pick_up = models.TextField(max_length=10, default='no')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class Message(models.Model):
    sender = models.ForeignKey('auth.User', related_name='sent_messages')
    receiver = models.ForeignKey('auth.User', related_name='received_messages')
    create_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=1000, blank=False, null=False)
