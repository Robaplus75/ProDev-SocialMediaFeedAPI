import graphene
from .types import PostType, CommentType
from ..models import Post, Comment
from django.contrib.auth.models import User


class CreatePost(graphene.Mutation):
    """Mutation to create a new post."""
    class Arguments:
        user_id = graphene.ID(required=True)
        content = graphene.String(required=True)

    post = graphene.Field(PostType)
    error = graphene.String()

    def mutate(self, info, user_id, content):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return CreatePost(post=None, error="User  not found.")

        post = Post(user=user, content=content)
        post.save()
        return CreatePost(post=post, error=None)


class UpdatePost(graphene.Mutation):
    """Mutation to update an existing post."""
    class Arguments:
        id = graphene.ID(required=True)
        content = graphene.String()

    post = graphene.Field(PostType)
    error = graphene.String()

    def mutate(self, info, id, content):
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return UpdatePost(post=None, error="Post not found.")

        if content:
            post.content = content
        post.save()
        return UpdatePost(post=post, error=None)


class DeletePost(graphene.Mutation):
    """Mutation to delete a post."""
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, id):
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return DeletePost(success=False, error="Post not found.")

        post.delete()
        return DeletePost(success=True, error=None)


class CreateComment(graphene.Mutation):
    """Mutation to create a new comment."""
    class Arguments:
        post_id = graphene.ID(required=True)
        user_id = graphene.ID(required=True)
        content = graphene.String(required=True)

    comment = graphene.Field(CommentType)
    error = graphene.String()

    def mutate(self, info, post_id, user_id, content):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return CreateComment(comment=None, error="Post not found.")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return CreateComment(comment=None, error="User  not found.")

        comment = Comment(post=post, user=user, content=content)
        comment.save()
        return CreateComment(comment=comment, error=None)


class UpdateComment(graphene.Mutation):
    """Mutation to update an existing comment."""

    class Arguments:
        id = graphene.ID(required=True)
        content = graphene.String(required=True)

    comment = graphene.Field(CommentType)
    error = graphene.String()

    def mutate(self, info, id, content):
        try:
            comment = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            return UpdateComment(comment=None, error="Comment not found.")

        comment.content = content
        comment.save()
        return UpdateComment(comment=comment, error=None)


class DeleteComment(graphene.Mutation):
    """Mutation to delete a comment."""

    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, id):
        try:
            comment = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            return DeleteComment(success=False, error="Comment not found.")

        comment.delete()
        return DeleteComment(success=True, error=None)


class Mutation(graphene.ObjectType):
    """Mutation class to define all mutations."""

    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
    create_comment = CreateComment.Field()
    update_comment = UpdateComment.Field()
    delete_comment = DeleteComment.Field()
