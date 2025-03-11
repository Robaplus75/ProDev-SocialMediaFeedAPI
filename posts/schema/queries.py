import graphene
from graphene_django.types import DjangoObjectType
from .types import PostType, CommentType
from interactions.schema.types import InteractionTypeEnum
from ..models import Post, Comment
from django.db.models import Q


class Query(graphene.ObjectType):
    """Query class to define the available queries."""
    all_posts = graphene.List(
        PostType,
        first=graphene.Int(),
        after=graphene.String(),
        title_contains=graphene.String(),
        content_contains=graphene.String(),
        interactions_count_above=graphene.Int(),
        interactions_count_below=graphene.Int(),
        interaction_type=InteractionTypeEnum(),
        by_author_username=graphene.String(),
        created_after=graphene.DateTime(),
        created_before=graphene.DateTime(),
    )
    post = graphene.Field(PostType, id=graphene.ID(required=True))
    comments_for_post = graphene.List(
        CommentType,
        post_id=graphene.ID(required=True)
    )

    def resolve_all_posts(
        self,
        info,
        first=None,
        after=None,
        title_contains=None,
        content_contains=None,
        interactions_count_above=None,
        interactions_count_below=None,
        interaction_type=None,
        by_author_username=None,
        created_after=None,
        created_before=None,
    ):
        """Resolve all posts with pagination and filtering."""
        queryset = Post.objects.all()

        # Implement pagination
        if after:
            last_post_id = int(after)
            queryset = queryset.filter(id__gt=last_post_id)

        # Filter by title
        if title_contains:
            queryset = queryset.filter(title__icontains=title_contains)

        # Filter by content
        if content_contains:
            queryset = queryset.filter(content__icontains=content_contains)

        # Filter by interactions count
        if interactions_count_above is not None:
            queryset = queryset.filter(
                    interactions_count__gt=interactions_count_above
            )

        if interactions_count_below is not None:
            queryset = queryset.filter(
                    interactions_count__lt=interactions_count_below
            )

        # Filter by interaction type (if applicable)
        if interaction_type:
            # Assuming you have a way to relate posts to interactions
            queryset = queryset.filter(
                    interactions__interaction_type=interaction_type.value
            )

        # Filter by author (username)
        if by_author_username:
            queryset = queryset.filter(user__username=by_author_username)
        # Filter by created date
        if created_after:
            queryset = queryset.filter(created_at__gte=created_after)

        if created_before:
            queryset = queryset.filter(created_at__lte=created_before)

        if first:
            queryset = queryset[:first]

        return queryset

    def resolve_post(self, info, id):
        """Resolve a specific post by ID."""
        return Post.objects.get(id=id)

    def resolve_comments_for_post(self, info, post_id):
        """Resolve comments for a specific post."""
        return Comment.objects.filter(post_id=post_id)
