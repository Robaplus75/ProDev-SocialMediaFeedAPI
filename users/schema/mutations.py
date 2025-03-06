import graphene
from django.contrib.auth import get_user_model
from graphql_jwt.shortcuts import get_token
from .types import UserType
from django.core.exceptions import ValidationError
from django.db import IntegrityError
import graphql_jwt

User = get_user_model()


class CreateUser(graphene.Mutation):
    """ Mutation to create a new user."""

    user = graphene.Field(UserType)
    success = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(
            self, info, username, password,
            first_name, email, last_name=None
    ):
        user = User(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email
        )
        user.set_password(password)
        try:
            user.full_clean()
            user.save()
            return CreateUser(user=user, success=True, error=None)
        except ValidationError as e:
            return CreateUser(user=None, success=False, error=str(e))
        except IntegrityError:
            return CreateUser(
                    user=None,
                    success=False,
                    error="An error occurred while saving the user."
            )


class LoginUser(graphene.Mutation):
    """ Mutation to login a user."""

    token = graphene.String()
    user = graphene.Field(UserType)
    error = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        user = User.objects.filter(username=username).first()
        if not user:
            return LoginUser(
                    token=None,
                    user=None,
                    error="User  not found."
            )

        if not user.check_password(password):
            return LoginUser(
                    token=None,
                    user=None,
                    error="Incorrect password."
            )
        # If Login is Successful
        return LoginUser(
                token=get_token(user),
                user=user,
                error=None
        )


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    create_user = CreateUser.Field()
    login_user = LoginUser.Field()
