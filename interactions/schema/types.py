import graphene
from graphene_django.types import DjangoObjectType
from .models import Interaction

class InteractionType(DjangoObjectType):
    class Meta:
        model = Interaction
        fields = ('id', 'user', 'post', 'interaction_type', 'created_at')
