from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """
    Represents a post made by a user in the social media feed.

    Attributes:
        user (ForeignKey): The user who created the post.
        content (TextField): The content of the post.
        created_at (DateTimeField): Timestamp when the post was created.
        updated_at (DateTimeField): Timestamp when the post was last updated.
        likes_count (PositiveIntegerField): A count of likes for the post.
        comments_count (PositiveIntegerField):A count of comments for the post
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']  # default ordering: most recent posts first
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at}"


class Comment(models.Model):

    """
    Represents a comment made by a user on a post.

    Attributes:
        post (ForeignKey): The post that the comment belongs to.
        user (ForeignKey): The user who created the comment.
        content (TextField): The content of the comment.
        created_at (DateTimeField): Timestamp when the comment was created.
    """
    post = models.ForeignKey(
            Post,
            on_delete=models.CASCADE,
            related_name='comments'
    )
    user = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Meta options for the Comment model.
        """
        ordering = ['created_at']  # Default ordering: oldest comments first
        indexes = [
            models.Index(fields=['post']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.id}"
