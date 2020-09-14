import graphene
from graphene import relay
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField

from shipment.models import Shipment, Package


class PackageNode(DjangoObjectType):
    class Meta:
        model = Package
        interfaces = [relay.Node, ]


class ShipmentNode(DjangoObjectType):
    class Meta:
        model = Shipment
        interfaces = [relay.Node, ]
        filter_fields = ['status']


class Query(graphene.ObjectType):
    shipments = DjangoFilterConnectionField(ShipmentNode)