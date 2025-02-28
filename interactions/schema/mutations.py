import graphene
from .types import InteractionType
from ..models import Interaction
from posts.models import Post


class AddInteraction(graphene.Mutation):
    """Mutation to add an interaction (like/dislike) to a post."""

    class Arguments:
        post_id = graphene.Int(required=True, description="ID of the post.")
        interaction_type = graphene.String(
            required=True,
            description="Type of interaction."
        )

    success = graphene.Boolean(
        description="Indicates if the interaction was added."
    )
    message = graphene.String(description="Additional information.")
    interaction = graphene.Field(
        InteractionType,
        description="The created interaction object."
    )

    def mutate(self, info, post_id, interaction_type):
        """Add an interaction to a post."""
        user = info.context.user
        if not user.is_authenticated:
            return AddInteraction(
                success=False,
                message="User  must be logged in."
            )

        # Validate interaction_type against allowed choices
        allowed_interaction_types = dict(Interaction.INTERACTION_TYPES)
        if interaction_type not in allowed_interaction_types:
            return AddInteraction(
                success=False,
                message=(
                    f"Invalid interaction type. Must be one of: "
                    f"{', '.join(allowed_interaction_types.keys())}."
                )
            )

        post = Post.objects.get(id=post_id)

        # Check if the user already has an interaction of the same type for this post
        existing_interaction = Interaction.objects.filter(
            user=user,
            post=post,
            interaction_type=interaction_type
        ).first()

        if existing_interaction:
            return AddInteraction(
                success=False,
                message="User  has already added this type of interaction.",
                interaction=existing_interaction
            )

        # Create the new interaction
        interaction = Interaction(
            user=user,
            post=post,
            interaction_type=interaction_type
        )
        interaction.save()

        post.likes_count += 1
        post.save()

        return AddInteraction(
            success=True,
            message="Interaction added successfully.",
            interaction=interaction
        )

class RemoveInteraction(graphene.Mutation):
    """Mutation to remove an interaction from a post."""

    class Arguments:
        post_id = graphene.Int(required=True, description="ID of the post.")
        interaction_type = graphene.String(
                required=True,
                description="Type of interaction to remove."
        )

    success = graphene.Boolean(
            description="Indicates if the interaction was removed."
    )
    message = graphene.String(
            description="Additional information."
    )

    def mutate(self, info, post_id, interaction_type):
        """Remove an interaction from a post."""
        user = info.context.user
        if not user.is_authenticated:
            return RemoveInteraction(
                    success=False,
                    message="User  must be logged in."
            )

        # Validate interaction_type against allowed choices
        allowed_interaction_types = dict(Interaction.INTERACTION_TYPES)
        if interaction_type not in allowed_interaction_types:
            return AddInteraction(
                success=False,
                message=(
                    f"Invalid interaction type. Must be one of: "
                    f"{', '.join(allowed_interaction_types.keys())}."
                )
            )

        post = Post.objects.get(id=post_id)

        try:
            interaction = Interaction.objects.get(
                user=user,
                post=post,
                interaction_type=interaction_type
            )
            interaction.delete()
            post.likes_count -= 1
            post.save()
            return RemoveInteraction(
                    success=True,
                    message="Interaction removed successfully."
            )
        except Interaction.DoesNotExist:
            return RemoveInteraction(
                    success=False,
                    message="Interaction does not exist."
            )


class Mutation(graphene.ObjectType):
    """Root mutation class for interactions."""

    add_interaction = AddInteraction.Field()
    remove_interaction = RemoveInteraction.Field()
