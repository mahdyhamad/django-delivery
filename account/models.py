from django.db import models
from django.contrib.auth.models import AbstractUser
from model_utils.models import TimeStampedModel


class User(AbstractUser):
    full_name = models.TextField(null=True, blank=True)


class UserProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_shop = models.BooleanField(default=False)
    client = models.ForeignKey('client.Client', blank=True, null=True, on_delete=models.PROTECT)
    mobile_number = models.TextField(null=True, blank=True)
