from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    pic = models.FileField(upload_to='images/pic')
    pic_id = models.FileField(upload_to='images/pic_id')


class Event(models.Model):
    create_by = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='events')
    content = models.TextField(max_length=500)
    close_time = models.DateTimeField()
    event_time = models.DateTimeField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class SignUp(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='signups')
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='signups')
    is_pick_up = models.TextField(max_length=10)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
