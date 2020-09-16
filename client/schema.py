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
            'id': ['exact', ],
            'detailed_address': ['icontains', ]
        }


class Query(graphene.ObjectType):
    clients = DjangoFilterConnectionField(ClientNode)
    client = graphene.Field(ClientNode, id=graphene.ID(required=True))

    @login_required
    def resolve_clients(self, info, *args, **kwargs):
        return Client.objects.all()

    @login_required
    def resolve_client(self, info, id):
        client= relay.Node.get_node_from_global_id(info, id, ClientNode)
        try:
            return Client.objects.get(id__exact=client.id)

        except:
            raise Exception("Provide correct Client ID")
