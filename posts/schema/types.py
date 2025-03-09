import graphene
from graphene_django.types import DjangoObjectType
from ..models import Post, Comment, Share
from django.contrib.auth import get_user_model

User = get_user_model()


class UserType(DjangoObjectType):
    """GraphQL type for the User model."""
    class Meta:
        model = User


class PostType(DjangoObjectType):
    """GraphQL type for the Post model."""
    class Meta:
        model = Post


class CommentType(DjangoObjectType):
    """GraphQL type for the Comment model."""
    class Meta:
        model = Comment


class ShareType(DjangoObjectType):
    """GraphQL type for the Share model."""
    class Meta:
        model = Share
