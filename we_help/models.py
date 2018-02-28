from django.db import models
# Create your models here.


class Event(models.Model):
    create_user = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name='events')
    content = models.TextField(max_length=500)
    close_time = models.DateTimeField(null=True)
    event_time = models.DateTimeField(null=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=False)
    address = models.TextField(max_length=200, blank=True, default='')


class SignUp(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='signups')
    signup_user = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name='signups')
    is_pick_up = models.TextField(max_length=10)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class Message(models.Model):
    sender = models.ForeignKey('auth.User', related_name='sent_messages')
    receiver = models.ForeignKey('auth.User', related_name='received_messages')
    create_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=1000, blank=False, null=False)
