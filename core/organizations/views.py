from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Organization, OrganizationMember
from .serializers import (
    OrganizationSerializer,
    OrganizationMemberSerializer,
    OrganizationMemberCreateSerializer,
    OrganizationMemberUpdateSerializer,
)
from .permissions import IsOrganizationOwner, IsOrganizationMember

User = get_user_model()


class OrganizationCreateView(generics.CreateAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class OrganizationListView(generics.ListAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Organization.objects.filter(created_by=self.request.user)


class OrganizationDetailView(generics.RetrieveAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Organization.objects.filter(created_by=self.request.user)


class OrganizationUpdateView(generics.UpdateAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Organization.objects.filter(created_by=self.request.user)


class OrganizationDeleteView(generics.DestroyAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Organization.objects.filter(created_by=self.request.user)


class OrganizationMemberCreateView(generics.CreateAPIView):
    serializer_class = OrganizationMemberCreateSerializer
    permission_classes = [
        IsAuthenticated,
        IsOrganizationOwner,
    ]

    def get_serializer_context(self):
        context = super().get_serializer_context()

        organization = Organization.objects.get(id=self.kwargs["organization_id"])

        context["organization"] = organization

        return context


class OrganizationMemberListView(generics.ListAPIView):
    serializer_class = OrganizationMemberSerializer
    permission_classes = [
        IsAuthenticated,
        IsOrganizationMember,
    ]

    def get_queryset(self):
        organization_id = self.kwargs["organization_id"]

        return OrganizationMember.objects.filter(
            organization_id=organization_id,
        )


class OrganizationMemberDeleteView(generics.DestroyAPIView):
    serializer_class = OrganizationMemberSerializer
    permission_classes = [
        IsAuthenticated,
        IsOrganizationOwner,
    ]

    def get_queryset(self):
        organization_id = self.kwargs["organization_id"]

        return OrganizationMember.objects.filter(
            organization_id=organization_id,
            organization__created_by=self.request.user,
        )


class OrganizationMemberUpdateView(generics.UpdateAPIView):
    serializer_class = OrganizationMemberUpdateSerializer
    permission_classes = [
        IsAuthenticated,
        IsOrganizationOwner,
    ]

    def get_queryset(self):
        organization_id = self.kwargs["organization_id"]

        return OrganizationMember.objects.filter(
            organization_id=organization_id,
            organization__created_by=self.request.user,
        )
