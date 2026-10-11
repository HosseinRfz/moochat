from rest_framework.permissions import BasePermission


class IsConversationOwner(BasePermission):
    message = "You do not have permission to access this conversation."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsMessageConversationOwner(BasePermission):
    message = "You do not have permission to access this message."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj.conversation.user == request.user
