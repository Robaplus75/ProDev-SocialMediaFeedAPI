from django.test import TestCase
from django.contrib.auth import get_user_model
from posts.models import Post
from ..models import Interaction

User = get_user_model()


class InteractionModelTest(TestCase):
    """
    Test case for the Interaction model.
    """

    def setUp(self):
        """
        Set up a user and a post instance for testing.
        """
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.post = Post.objects.create(
            user=self.user, content='This is a test post.'
        )
        self.interaction_like = Interaction.objects.create(
            user=self.user,
            post=self.post,
            interaction_type='like'
        )
        self.interaction_dislike = Interaction.objects.create(
            user=self.user,
            post=self.post,
            interaction_type='dislike'
        )

    def test_interaction_creation(self):
        """
        Test that an interaction is created correctly with
        the expected attributes.
        """
        self.assertEqual(self.interaction_like.user, self.user)
        self.assertEqual(self.interaction_like.post, self.post)
        self.assertEqual(self.interaction_like.interaction_type, 'like')
        self.assertIsNotNone(self.interaction_like.created_at)

    def test_unique_interaction_constraint(self):
        """
        Test that a user can only interact with a post once.
        """
        with self.assertRaises(Exception):
            Interaction.objects.create(
                user=self.user,
                post=self.post,
                interaction_type='like'
            )
