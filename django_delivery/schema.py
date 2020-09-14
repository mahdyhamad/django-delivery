import graphene
import graphql_jwt
from graphql_jwt.decorators import login_required
import account.schema
import shipment.schema
# import client.schema


class Query(account.schema.Query,
            # client.schema.Query,
            shipment.schema.Query,
            graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, info, *args, **kwargs):
        return "Hello Man"


class Mutation(
    account.schema.Mutation,
    graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)