import graphene
from .types import InteractionType
from .models import Interaction


class Query(graphene.ObjectType):
    interactions = graphene.List(
            InteractionType,
            user_id=graphene.Int(),
            post_id=graphene.Int())

    def resolve_interactions(self, info, user_id=None, post_id=None):
        qs = Interaction.objects.all()
        if user_id:
            qs = qs.filter(user__id=user_id)
        if post_id:
            qs = qs.filter(post__id=post_id)
        return qs
