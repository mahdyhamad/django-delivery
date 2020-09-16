import graphene
from graphene import relay
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

from account.schema import UserNode
from client.schema import ClientNode
from credentials.models import Credentials
from shipment.models import Shipment, Package


class PackageNode(DjangoObjectType):
    class Meta:
        model = Package
        interfaces = [relay.Node, ]


class CredentialsNode(DjangoObjectType):
    class Meta:
        model = Credentials


class ShipmentNode(DjangoObjectType):
    credentials = graphene.Field(CredentialsNode)

    class Meta:
        model = Shipment
        interfaces = [relay.Node, ]
        filter_fields = {
            'status': ['exact', ],
            'id': ['exact', ]
        }


class Query(graphene.ObjectType):
    shipments = DjangoFilterConnectionField(ShipmentNode)


class CreatePackage(graphene.Mutation):
    package = graphene.Field(PackageNode)

    class Arguments:
        size = graphene.String(required=True)
        weight = graphene.Decimal(required=True)

    @login_required
    def mutate(self, info, size, weight):

        package = Package.objects.create(size=size, weight=weight)
        return CreatePackage(package=package)


class CreateShipment(graphene.Mutation):
    shipment = graphene.Field(ShipmentNode)

    class Arguments:
        client_id = graphene.ID(required=True)
        pickup_user_id = graphene.ID(required=True)
        package_id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, client_id, pickup_user_id, package_id):
        import pdb
        pdb.set_trace()
        client = relay.Node.get_node_from_global_id(info, client_id, ClientNode)
        pickup_user = relay.Node.get_node_from_global_id(info, pickup_user_id, UserNode)
        drop_user = info.context.user
        package = relay.Node.get_node_from_global_id(info, package_id, PackageNode)

        shipment = Shipment.create(
            client=client, package=package, pickup_user=pickup_user, drop_off_user=drop_user)

        return CreateShipment(shipment=shipment)


class DeleteShipment(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        shipment_id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, shipment_id, *args, **kwargs):
        shipment = relay.Node.get_node_from_global_id(info, shipment_id, ShipmentNode)
        shipment.delete()
        return DeleteShipment(success=True)


class Mutation(object):
    create_shipment = CreateShipment.Field()
    delete_shipment = DeleteShipment.Field()
    create_package = CreatePackage.Field()

