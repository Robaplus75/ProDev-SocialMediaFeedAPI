import graphene
from graphql import GraphQLError
from .types import UserType


class Query(graphene.ObjectType):
    """GraphQL query to retrieve the currently logged-in user."""

    logged_user = graphene.Field(UserType)

    def resolve_logged_user(self, info):
        """Resolve the logged-in user"""

        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError("Not authenticated!")
        return user
