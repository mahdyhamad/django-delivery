import uuid
from django.db import models
from model_utils.models import TimeStampedModel
from account.models import User
from credentials.models import Credentials


class SizeChoices(object):
    small = 'small'
    medium = 'medium'
    large = 'large'


class Package(TimeStampedModel):
    SIZE_CHOICES = (
        (SizeChoices.small, 'small'),
        (SizeChoices.medium, 'medium'),
        (SizeChoices.large, 'large')
    )
    id = models.UUIDField(primary_key=True, unique=True, auto_created=True, default=uuid.UUID)
    size = models.TextField(choices=SIZE_CHOICES)
    weight = models.FloatField(null=True, blank=True)


class ShipmentStatusChoices(object):
    draft = 'draft'
    dropped = 'dropped'
    picked_up = 'picked up'


class Shipment(TimeStampedModel):
    SHIPMENT_STATUS_CHOICES = (
        (ShipmentStatusChoices.draft, 'draft'),
        (ShipmentStatusChoices.dropped, 'dropped'),
        (ShipmentStatusChoices.picked_up, 'picked up'),
    )
    id = models.UUIDField(primary_key=True, unique=True, auto_created=True, default=uuid.UUID)
    client = models.ForeignKey('client.Client', on_delete=models.CASCADE, related_name="related_shipments", null=True, blank=True)
    drop_off_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='related_drop_off_shipments')
    pickup_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='related_pickup_shipments')
    package = models.OneToOneField(Package, on_delete=models.PROTECT)
    credentials = models.OneToOneField(Credentials, on_delete=models.PROTECT)
    status = models.CharField(max_length=9, choices=SHIPMENT_STATUS_CHOICES)

