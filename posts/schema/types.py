import graphene
from graphene_django.types import DjangoObjectType
from ..models import Post, Comment
from django.contrib.auth.models import User


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
