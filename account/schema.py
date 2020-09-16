import graphene
from django.contrib.auth import get_user_model
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required
from account.filters import UserFilter
from account.models import UserProfile, User


class UserNode(DjangoObjectType):
    class Meta:
        model = get_user_model()
        interfaces = [relay.Node, ]


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserNode)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        mobile_number = graphene.String(required=False)
        is_shop = graphene.Boolean(required=False)

    def mutate(self, info, username, password, first_name, last_name, is_shop=False, mobile_number=""):
        first_name = first_name.capitalize()
        last_name = last_name.capitalize()
        try:

            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                full_name=first_name + " " + last_name,
            )
            profile = UserProfile.objects.get_or_create(user=user, mobile_number=mobile_number)
            return CreateUser(user=user)

        except:
            raise Exception("User Already exists")


class Query(graphene.ObjectType):
    users = DjangoFilterConnectionField(UserNode, filterset_class=UserFilter)
    me = graphene.Field(UserNode)

    @login_required
    def resolve_me(self, info, *args, **kwargs):
        return info.context.user

    @login_required
    def resolve_users(self, info, *args, **kwargs):
        return User.objects.filter(is_shop=False, is_staff=False).exclude(id=info.context.user.id)


class Mutation(object):
    create_user = CreateUser.Field()
