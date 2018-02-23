from django.db import models
# Create your models here.


class Event(models.Model):
    create_by = models.ForeignKey(
        "accounts.Profile", on_delete=models.CASCADE, related_name='events')
    content = models.TextField(max_length=500)
    close_time = models.DateTimeField()
    event_time = models.DateTimeField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class SignUp(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='signups')
    profile = models.ForeignKey(
        "accounts.Profile", on_delete=models.CASCADE, related_name='signups')
    is_pick_up = models.TextField(max_length=10)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
