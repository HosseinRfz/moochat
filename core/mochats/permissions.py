from rest_framework.permissions import BasePermission


class IsOrganizationAdmin(BasePermission):
    message = "Only organization admins can perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj.moochat.organization.members.filter(
            user=request.user,
            role="admin",
        ).exists()


class IsKnowledgeItemOrganizationAdmin(BasePermission):
    message = "Only organization admins can perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj.knowledge_base.moochat.organization.members.filter(
            user=request.user,
            role="admin",
        ).exists()
