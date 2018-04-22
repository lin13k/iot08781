from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    pic = models.FileField(
        upload_to='images/pic', blank=True, default='')
    pic_id = models.FileField(
        upload_to='images/pic_id', blank=True, default='')
    phone = models.TextField(max_length=12, blank=True, null=True)
