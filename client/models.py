import uuid
from django.db import models
from django.db.models import Sum
from model_utils.models import TimeStampedModel
from account.models import User
from shipment.models import Shipment


class CityOptions(object):
    amman = 'Amman'
    irbid = 'Irbid'


class Client(TimeStampedModel):
    CITY_OPTIONS = (
        (CityOptions.amman, 'Amman'),
        (CityOptions.irbid, 'Irbid'),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    users = models.ManyToManyField(User)
    shipments = models.ManyToManyField(Shipment, related_name="related_clients")
    name = models.TextField()
    city = models.TextField(choices=CITY_OPTIONS, null=True, blank=True)
    detailed_address = models.TextField(null=True, blank=True)

    @property
    def shipments_count(self):
        return Shipment.objects.filter(client__exact=self).count()

    @property
    def total_money_earned(self):

        return Shipment.objects.filter(client__exact=self).aggregate(Sum('price'))['price__sum']

    def __str__(self):
        return self.name