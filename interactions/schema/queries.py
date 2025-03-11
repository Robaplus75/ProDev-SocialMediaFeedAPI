import graphene
from .types import InteractionType
from ..models import Interaction


class Query(graphene.ObjectType):
    interactions = graphene.List(
            InteractionType,
            username=graphene.String(),
            post_id=graphene.Int())

    def resolve_interactions(self, info, username=None, post_id=None):
        qs = Interaction.objects
        if username:
            qs = qs.filter(user__username=username)
        if post_id:
            qs = qs.filter(post__id=post_id)
        return qs.all()
