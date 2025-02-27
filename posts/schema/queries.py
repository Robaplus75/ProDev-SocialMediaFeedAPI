import graphene
from .types import PostType, CommentType
from ..models import Post, Comment


class Query(graphene.ObjectType):
    """Query class to define the available queries."""
    all_posts = graphene.List(PostType)
    post = graphene.Field(PostType, id=graphene.ID(required=True))
    comments_for_post = graphene.List(
            CommentType,
            post_id=graphene.ID(required=True)
    )

    def resolve_all_posts(self, info):
        return Post.objects.all()

    def resolve_post(self, info, id):
        return Post.objects.get(id=id)

    def resolve_comments_for_post(self, info, post_id):
        return Comment.objects.filter(post_id=post_id)
