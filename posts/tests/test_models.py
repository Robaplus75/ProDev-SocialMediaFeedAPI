from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Post, Comment

User = get_user_model()


class PostModelTest(TestCase):
    """
    Test case for the Post model.
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

    def test_post_creation(self):
        """
        Test that a post is created correctly with the expected attributes.
        """
        self.assertEqual(self.post.user, self.user)
        self.assertEqual(self.post.content, 'This is a test post.')
        self.assertEqual(self.post.likes_count, 0)  # Default value
        self.assertEqual(self.post.comments_count, 0)  # Default value

    def test_post_string_representation(self):
        """
        Test the string representation of the post.
        """
        expected_str = (
            f"Post by {self.user.username} at {self.post.created_at}"
        )
        self.assertEqual(str(self.post), expected_str)


class CommentModelTest(TestCase):
    """
    Test case for the Comment model.
    """

    def setUp(self):
        """
        Set up a user, a post, and a comment instance for testing.
        """
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.post = Post.objects.create(
            user=self.user, content='This is a test post.'
        )
        self.comment = Comment.objects.create(
            post=self.post, user=self.user,
            content='This is a test comment.'
        )

    def test_comment_creation(self):
        """
        Test that a comment is created correctly with the expected attributes.
        """
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.content, 'This is a test comment.')

    def test_comment_string_representation(self):
        """
        Test the string representation of the comment.
        """
        expected_str = (
            f"Comment by {self.user.username} on {self.post.id}"
        )
        self.assertEqual(str(self.comment), expected_str)
