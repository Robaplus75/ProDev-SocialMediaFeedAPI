import graphene

from users.schema.queries import Query as UsersQuery
from posts.schema.queries import Query as PostsQuery
from interactions.schema.queries import Query as InteractionsQuery

from users.schema.mutations import Mutation as UsersMutation
from posts.schema.mutations import Mutation as PostsMutation
from interactions.schema.mutations import Mutation as InteractionsMutation


class Query(UsersQuery, PostsQuery, InteractionsQuery, graphene.ObjectType):
    """Combined query class for posts and interactions."""
    pass


class Mutation(
        UsersMutation,
        PostsMutation,
        InteractionsMutation,
        graphene.ObjectType
):
    """Combined mutation class for posts and interactions."""
    pass


# Create the combined schema
schema = graphene.Schema(query=Query, mutation=Mutation)
