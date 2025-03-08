import graphene
from .types import InteractionType, InteractionTypeEnum
from ..models import Interaction
from posts.models import Post


class AddInteraction(graphene.Mutation):
    """Mutation to add an interaction (like/dislike) to a post."""

    class Arguments:
        post_id = graphene.Int(required=True, description="ID of the post.")
        interaction_type = InteractionTypeEnum(
                required=True,
                description="Type of interaction."
        )

    success = graphene.Boolean(
        description="Indicates if the interaction was added."
    )
    error = graphene.String(
            description="Error message if the operation failed."
    )
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
                error="User  must be logged in."
            )

        # Validate interaction_type against allowed choices
        allowed_interaction_types = dict(Interaction.INTERACTION_TYPES)
        if interaction_type not in allowed_interaction_types:
            return AddInteraction(
                success=False,
                error=(
                    f"Invalid interaction type. Must be one of: "
                    f"{', '.join(allowed_interaction_types.keys())}."
                )
            )

        post = Post.objects.filter(id=post_id).first()
        if not post:
            return AddInteraction(success=False, error="Post not found.")

        # Check if the user already has an interaction of the same type
        existing_interaction = Interaction.objects.filter(
            user=user,
            post=post,
            interaction_type=interaction_type
        ).first()

        if existing_interaction:
            return AddInteraction(
                success=False,
                error="User  has already added this type of interaction.",
                interaction=existing_interaction
            )

        # Create the new interaction
        interaction = Interaction(
            user=user,
            post=post,
            interaction_type=interaction_type
        )
        interaction.save()

        post.save()
        post.interactions_count += 1

        return AddInteraction(
            success=True,
            error=None,
            interaction=interaction
        )


class RemoveInteraction(graphene.Mutation):
    """Mutation to remove an interaction from a post."""

    class Arguments:
        post_id = graphene.Int(required=True, description="ID of the post.")
        interaction_type = InteractionTypeEnum(
                required=True,
                description="Type of interaction."
        )

    success = graphene.Boolean(
            description="Indicates if the interaction was removed."
    )
    error = graphene.String(
            description="Error message if the operation failed."
    )

    def mutate(self, info, post_id, interaction_type):
        """Remove an interaction from a post."""
        user = info.context.user

        # Check if User is Authenticated
        if not user.is_authenticated:
            return RemoveInteraction(
                    success=False,
                    error="User  must be logged in."
            )

        # Validate interaction_type against allowed choices
        allowed_interaction_types = dict(Interaction.INTERACTION_TYPES)
        if interaction_type not in allowed_interaction_types:
            return RemoveInteraction(
                success=False,
                error=(
                    f"Invalid interaction type. Must be one of: "
                    f"{', '.join(allowed_interaction_types.keys())}."
                )
            )

        post = Post.objects.filter(id=post_id).first()

        try:
            interaction = Interaction.objects.get(
                user=user,
                post=post,
                interaction_type=interaction_type
            )

            interaction.delete()
            post.interactions_count -= 1
            post.save()

            return RemoveInteraction(
                    success=True,
                    error=None
            )
        except Interaction.DoesNotExist:
            return RemoveInteraction(
                    success=False,
                    error="Interaction does not exist."
            )


class Mutation(graphene.ObjectType):
    """Root mutation class for interactions."""

    add_interaction = AddInteraction.Field(name="Post_Interaction_Add")
    remove_interaction = RemoveInteraction.Field(
                                name="Post_Interaction_Remove"
                        )
