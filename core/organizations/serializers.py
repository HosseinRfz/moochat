from rest_framework import serializers

from .models import Organization, OrganizationMember
from django.contrib.auth import get_user_model

User = get_user_model()


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_by",
            "created_at",
            "updated_at",
        ]


class OrganizationMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationMember
        fields = [
            "id",
            "organization",
            "user",
            "role",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class OrganizationMemberUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationMember
        fields = [
            "role",
        ]


class OrganizationMemberCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)

    class Meta:
        model = OrganizationMember
        fields = [
            "username",
            "role",
        ]

    def validate_username(self, value):
        try:
            user = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "A user with this username does not exist."
            )

        if OrganizationMember.objects.filter(
            organization=self.context["organization"],
            user=user,
        ).exists():
            raise serializers.ValidationError(
                "This user is already a member of the organization."
            )

        return value

    def create(self, validated_data):
        username = validated_data.pop("username")
        organization = self.context["organization"]

        user = User.objects.get(username=username)

        member = OrganizationMember.objects.create(
            organization=organization,
            user=user,
            **validated_data,
        )

        return member
