from rest_framework.permissions import BasePermission

from .models import Organization, OrganizationMember


class IsOrganizationOwner(BasePermission):

    def has_permission(self, request, view):
        organization_id = view.kwargs.get("organization_id")

        if not organization_id:
            return False

        return Organization.objects.filter(
            id=organization_id,
            created_by=request.user,
        ).exists()


class IsOrganizationMember(BasePermission):

    def has_permission(self, request, view):
        organization_id = view.kwargs.get("organization_id")

        if not organization_id:
            return False

        return OrganizationMember.objects.filter(
            organization_id=organization_id,
            user=request.user,
        ).exists()
