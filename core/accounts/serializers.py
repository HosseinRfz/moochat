from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)

    def validate_phone_number(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Phone number is required.")

        return value


class CompleteRegistrationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    organization_name = serializers.CharField(max_length=255)
    website = serializers.URLField(
        required=False,
        allow_blank=True,
    )
    email = serializers.EmailField()

    def validate_phone_number(self, value):
        value = value.strip()

        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(
                "This phone number is already registered."
            )

        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("This email is already registered.")

        return value


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    verification_code = serializers.CharField(
        min_length=6,
        max_length=6,
    )
