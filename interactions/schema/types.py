import graphene
from graphene_django.types import DjangoObjectType
from ..models import Interaction


class InteractionType(DjangoObjectType):
    class Meta:
        model = Interaction
        fields = ('id', 'user', 'post', 'interaction_type', 'created_at')


class InteractionTypeEnum(graphene.Enum):
    """Enum for interaction types."""
    THUMBS_UP = 'thumbs_up'  # Represents a positive reaction
    THUMBS_DOWN = 'thumbs_down'  # Represents a negative reaction
    LOVE = 'love'  # Represents a love reaction
    HAHA = 'haha'  # Represents a laughter reaction
    WOW = 'wow'  # Represents a surprise reaction
    SAD = 'sad'  # Represents a sad reaction
    ANGRY = 'angry'  # Represents an angry reaction
