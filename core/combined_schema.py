import graphene

from posts.schema.queries import Query as PostsQuery
from interactions.schema.queries import Query as InteractionsQuery

from posts.schema.mutations import Mutation as PostsMutation
from interactions.schema.mutations import Mutation as InteractionsMutation


class Query(PostsQuery, InteractionsQuery, graphene.ObjectType):
    """Combined query class for posts and interactions."""
    pass


class Mutation(PostsMutation, InteractionsMutation, graphene.ObjectType):
    """Combined mutation class for posts and interactions."""
    pass


# Create the combined schema
schema = graphene.Schema(query=Query, mutation=Mutation)
