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

        # Check if User is Authenticated
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
        title = graphene.String()

    post = graphene.Field(PostType)
    error = graphene.String()
    success = graphene.Boolean()

    def mutate(self, info, post_id, content, title):
        # Get the currently logged-in user from the context
        user = info.context.user

        # Check if the user is authenticated
        if user.is_anonymous:
            return UpdatePost(
                post=None,
                error="User is not Authenticated",
                success=False
            )

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return UpdatePost(
                    post=None,
                    error="Post not found.",
                    success=False
            )

        # Check if the user is the author of the post
        if post.user != user:
            return UpdatePost(
                post=None,
                error="""
                    Logged User Does Not Have Permission to Update This Post
                """,
                success=False
            )

        # Update the post content and title if provided
        if content:
            post.content = content
        if title:
            post.title = title
        post.save()

        return UpdatePost(post=post, error=None, success=True)


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
            return DeletePost(
                error="User is not Authenticated",
                success=False
            )

        # Check if post exist
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return DeletePost(success=False, error="Post not found.")

        # Check if the user is the author of the post
        if post.user != user:
            return DeletePost(
                error="""
                    Logged User Does Not Have Permission to Delete This Post
                """,
                success=False
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
    success = graphene.Boolean()

    def mutate(self, info, post_id, content):
        # Get the currently logged-in user from the context
        user = info.context.user

        # Check if User is Authenticated
        if user.is_anonymous:
            return CreateComment(
                comment=None,
                error="User is not Authenticated",
                success=False
            )

        # Check if Post exist
        try:
            post = Post.objects.filter(id=post_id).first()
        except Post.DoesNotExist:
            return CreateComment(
                    comment=None,
                    error="Post not found.",
                    success=False
            )

        comment = Comment(post=post, user=user, content=content)

        # Increment the comments count on the post
        post.comments_count += 1
        post.save()

        comment.save()
        return CreateComment(comment=comment, error=None, success=True)


class UpdateComment(graphene.Mutation):
    """Mutation to update an existing comment."""

    class Arguments:
        comment_id = graphene.ID(required=True)
        content = graphene.String(required=True)

    comment = graphene.Field(CommentType)
    error = graphene.String()
    success = graphene.Boolean()

    def mutate(self, info, comment_id, content):
        # Get the currently logged-in user from the context
        user = info.context.user

        # Check if the user is authenticated
        if user.is_anonymous:
            return UpdateComment(
                comment=None,
                error="User is not Authenticated",
                success=False
            )

        # Check if comment exist
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return UpdateComment(
                    comment=None,
                    success=False,
                    error="Comment not found."
            )

        # Check if the user is the author of the comment.
        if comment.user != user:
            return UpdateComment(
                post=None,
                error="""
                    Logged User Does Not Have Permission to Update This comment
                """,
                success=False
            )

        comment.content = content
        comment.save()
        return UpdateComment(comment=comment, error=None, success=True)


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
            return DeleteComment(
                comment=None,
                error="User is not Authenticated",
                success=False
            )

        # Check if comment exist
        try:
            comment = Comment.objects.filter(id=comment_id).first()
        except Comment.DoesNotExist:
            return UpdateComment(success=False, error="Comment not found.")

        # Check if the user is the author of the comment.
        if comment.user != user:
            return DeleteComment(
                error="""
                    Logged User Does Not Have Permission to Delete This comment
                """,
                success=False
            )

        post = comment.post
        comment.delete()

        # Decrement the comments count on the post
        post.comments_count -= 1
        post.save()

        return DeleteComment(success=True, error=None)


class Mutation(graphene.ObjectType):
    """Mutation class to define all mutations."""

    create_post = CreatePost.Field(name="PostCreate")
    update_post = UpdatePost.Field(name="PostUpdate")
    delete_post = DeletePost.Field(name="PostDelete")
    create_comment = CreateComment.Field(name="Post_Comment_Add")
    update_comment = UpdateComment.Field(name="Post_Comment_update")
    delete_comment = DeleteComment.Field(name="Post_Comment_Delete")
