from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


class Interaction(models.Model):
    """
    Represents a user interaction with a post, such as a like or comment.

    Attributes:
        user (ForeignKey): The user who interacted with the post.
        post (ForeignKey): The post that was interacted with.
        interaction_type (CharField): The type of interaction.
        created_at (DateTimeField): Timestamp when the interaction was created.
    """
    INTERACTION_TYPES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='interactions'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='interactions'
    )
    interaction_type = models.CharField(
        max_length=10,
        choices=INTERACTION_TYPES
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Meta options for the Interaction model.
        """
        # Default ordering: most recent interactions first
        ordering = ['-created_at']
        # Ensure a user can only interact once per post per type
        unique_together = ('user', 'post', 'interaction_type')

    def __str__(self):
        return (f"{self.user.username} {self.interaction_type}d "
                f"on post {self.post.id} at {self.created_at}")
