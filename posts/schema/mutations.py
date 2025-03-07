import graphene
from .types import PostType, CommentType
from ..models import Post, Comment
from django.contrib.auth import get_user_model
from graphql import GraphQLError
from graphene_file_upload.scalars import Upload

User = get_user_model()


class CreatePost(graphene.Mutation):
    """Mutation to create a new post."""
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        image = Upload(required=False)

    post = graphene.Field(PostType)
    error = graphene.String()
    success = graphene.Boolean()

    def mutate(self, info, title, content, image=None):
        user = info.context.user

        if user.is_anonymous:
            return CreatePost(
                post=None,
                error="User is not Authenticated",
                success=False
            )

        # Create the post using the authenticated user
        post = Post(user=user, content=content, image=image, title=title)
        post.save()
        return CreatePost(post=post, error=None, success=True)


class UpdatePost(graphene.Mutation):
    """Mutation to update an existing post."""

    class Arguments:
        post_id = graphene.ID(required=True)
        content = graphene.String()

    post = graphene.Field(PostType)
    error = graphene.String()
    success = graphene.Boolean()

    def mutate(self, info, post_id, content):
        # Get the currently logged-in user from the context
        user = info.context.user

        # Check if the user is authenticated
        if user.is_anonymous:
            raise GraphQLError("Not authenticated!")

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return UpdatePost(post=None, error="Post not found.")

        # Check if the user is the author of the post
        if post.user != user:
            raise GraphQLError(
                    "You do not have permission to update this post."
            )

        # Update the post content if provided
        if content:
            post.content = content
        post.save()

        return UpdatePost(post=post, error=None)


class DeletePost(graphene.Mutation):
    """Mutation to delete a post."""

    class Arguments:
        post_id = graphene.ID(required=True)

    success = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, post_id):
        # Get the currently logged-in user from the context
        user = info.context.user

        # Check if the user is authenticated
        if user.is_anonymous:
            raise GraphQLError("Not authenticated!")

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return DeletePost(success=False, error="Post not found.")

        # Check if the user is the author of the post
        if post.user != user:
            raise GraphQLError(
                    "You do not have permission to delete this post."
            )

        post.delete()
        return DeletePost(success=True, error=None)


class CreateComment(graphene.Mutation):
    """Mutation to create a new comment."""
    class Arguments:
        post_id = graphene.ID(required=True)
        content = graphene.String(required=True)

    comment = graphene.Field(CommentType)
    error = graphene.String()

    def mutate(self, info, post_id, content):
        # Get the currently logged-in user from the context
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError("Not authenticated!")

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return CreateComment(comment=None, error="Post not found.")

        comment = Comment(post=post, user=user, content=content)
        comment.save()
        return CreateComment(comment=comment, error=None)


class UpdateComment(graphene.Mutation):
    """Mutation to update an existing comment."""

    class Arguments:
        comment_id = graphene.ID(required=True)
        content = graphene.String(required=True)

    comment = graphene.Field(CommentType)
    error = graphene.String()

    def mutate(self, info, comment_id, content):
        # Get the currently logged-in user from the context
        user = info.context.user

        # Check if the user is authenticated
        if user.is_anonymous:
            raise GraphQLError("Not authenticated!")

        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return UpdateComment(success=False, error="Comment not found.")

        # Check if the user is the author of the comment.
        if comment.user != user:
            raise GraphQLError(
                    "You do not have permission to edit this comment"
            )

        comment.content = content
        comment.save()
        return UpdateComment(comment=comment, error=None)


class DeleteComment(graphene.Mutation):
    """Mutation to delete a comment."""

    class Arguments:
        comment_id = graphene.ID(required=True)

    success = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, comment_id):
        # Get the currently logged-in user from the context
        user = info.context.user

        # Check if the user is authenticated
        if user.is_anonymous:
            raise GraphQLError("Not authenticated!")

        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return UpdateComment(success=False, error="Comment not found.")

        # Check if the user is the author of the comment.
        if comment.user != user:
            raise GraphQLError(
                    "You do not have permission to delete this comment"
            )

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
