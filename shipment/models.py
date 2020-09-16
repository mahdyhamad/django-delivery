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
    id = models.UUIDField(primary_key=True, unique=True, auto_created=True, default=uuid.uuid4)
    size = models.TextField(choices=SIZE_CHOICES)
    weight = models.FloatField(null=True, blank=True)


class ShipmentStatusChoices(object):
    draft = 'draft'
    in_process = 'in process'
    dropped = 'dropped'
    picked_up = 'picked up'


class Shipment(TimeStampedModel):
    SHIPMENT_STATUS_CHOICES = (
        (ShipmentStatusChoices.draft, 'draft'),
        (ShipmentStatusChoices.in_process, 'in process'),
        (ShipmentStatusChoices.dropped, 'dropped'),
        (ShipmentStatusChoices.picked_up, 'picked up'),
    )
    id = models.UUIDField(primary_key=True, unique=True, auto_created=True, default=uuid.uuid4)
    client = models.ForeignKey('client.Client', on_delete=models.CASCADE, related_name="related_shipments", null=True, blank=True)
    drop_off_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='related_drop_off_shipments')
    pickup_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='related_pickup_shipments')
    package = models.OneToOneField(Package, on_delete=models.PROTECT)
    credentials = models.ForeignKey(Credentials, on_delete=models.PROTECT)
    status = models.CharField(max_length=10, choices=SHIPMENT_STATUS_CHOICES, default=ShipmentStatusChoices.draft)
    paid = models.BooleanField(default=False)
    price = models.FloatField(default=0)


    @classmethod
    def create(cls, client, drop_off_user, pickup_user, package, *args, **kwargs):
        price: float
        if package.size == SizeChoices.small and package.weight <= 1:
            price = 0.75
        elif package.size == SizeChoices.medium and (1 < package.weight <= 3):
            price = 1.0
        else:
            price = 1.5
        credentials = Credentials.create()
        return cls.objects.create(
            client=client, drop_off_user=drop_off_user, pickup_user=pickup_user, package=package, credentials=credentials,
            status=ShipmentStatusChoices.in_process, price=price)

