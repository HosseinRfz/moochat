from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from rest_framework import serializers

from .tokens import account_activation_token

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
        ]


class ActivateAccountSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        uidb64 = attrs["uidb64"]
        token = attrs["token"]

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

        except (
            User.DoesNotExist,
            ValueError,
            TypeError,
            OverflowError,
        ):
            raise serializers.ValidationError("The link is invalid.")

        if user.is_active:
            raise serializers.ValidationError("The account has already been activated.")

        if not account_activation_token.check_token(user, token):
            raise serializers.ValidationError("The token is invalid or expired.")

        attrs["user"] = user

        return attrs


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if not username or not password:
            raise serializers.ValidationError("Username and password are required.")

        user = authenticate(
            username=username,
            password=password,
        )

        if user is None:
            raise serializers.ValidationError("Invalid username or password.")

        if not user.is_active:
            raise serializers.ValidationError("This account is not active.")

        attrs["user"] = user

        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        uid = attrs["uid"]
        token = attrs["token"]

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)

        except (
            User.DoesNotExist,
            ValueError,
            TypeError,
            OverflowError,
        ):
            raise serializers.ValidationError("The link is invalid.")

        password_reset_token = PasswordResetTokenGenerator()

        if not password_reset_token.check_token(user, token):
            raise serializers.ValidationError("The token is invalid or expired.")

        attrs["user"] = user

        return attrs
