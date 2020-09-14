import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

from client.models import Client


class ClientNode(DjangoObjectType):
    class Meta:
        model = Client
        interfaces = [relay.Node, ]
        filter_fields = {
            'city': ['icontains', ],
            'name': ['icontains', ],
            'detailed_address': ['icontains', ]
        }


class Query(graphene.ObjectType):
    clients = DjangoFilterConnectionField(ClientNode)

    @login_required
    def resolve_clients(self, info, *args, **kwargs):
        return Client.objects.all()
