from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import MooChat
from .models import KnowledgeBase, KnowledgeItem
from .serializers import MooChatSerializer
from .serializers import KnowledgeBaseSerializer, KnowledgeItemSerializer
from .permissions import IsOrganizationAdmin, IsKnowledgeItemOrganizationAdmin
from .rag import delete_knowledge_item

from organizations.models import OrganizationMember


class MooChatCreateView(generics.CreateAPIView):
    serializer_class = MooChatSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        organization_id = self.request.data.get("organization")

        is_member = OrganizationMember.objects.filter(
            organization_id=organization_id,
            user=self.request.user,
        ).exists()

        if not is_member:

            raise PermissionDenied("You are not a member of this organization.")

        serializer.save(
            created_by=self.request.user,
        )


class MooChatListView(generics.ListAPIView):
    serializer_class = MooChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MooChat.objects.filter(
            organization__members__user=self.request.user
        ).distinct()


class MooChatDetailView(generics.RetrieveAPIView):
    serializer_class = MooChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MooChat.objects.filter(
            organization__members__user=self.request.user
        ).distinct()


class MooChatUpdateView(generics.UpdateAPIView):
    serializer_class = MooChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MooChat.objects.filter(created_by=self.request.user)


class MooChatDeleteView(generics.DestroyAPIView):
    serializer_class = MooChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MooChat.objects.filter(created_by=self.request.user)


class KnowledgeBaseListCreateView(generics.ListCreateAPIView):
    serializer_class = KnowledgeBaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return KnowledgeBase.objects.filter(
            moochat__organization__members__user=self.request.user
        )

    def perform_create(self, serializer):
        moochat = serializer.validated_data["moochat"]

        is_admin = moochat.organization.members.filter(
            user=self.request.user,
            role="admin",
        ).exists()

        if not is_admin:
            raise PermissionDenied(
                "Only organization admins can create a knowledge base."
            )

        serializer.save()


class KnowledgeBaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = KnowledgeBaseSerializer
    permission_classes = [
        IsAuthenticated,
        IsOrganizationAdmin,
    ]

    def get_queryset(self):
        return KnowledgeBase.objects.filter(
            moochat__organization__members__user=self.request.user
        )


class KnowledgeItemListCreateView(generics.ListCreateAPIView):
    serializer_class = KnowledgeItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return KnowledgeItem.objects.filter(
            knowledge_base__moochat__organization__members__user=self.request.user
        )

    def perform_create(self, serializer):
        knowledge_base = serializer.validated_data["knowledge_base"]

        is_admin = knowledge_base.moochat.organization.members.filter(
            user=self.request.user,
            role="admin",
        ).exists()

        if not is_admin:
            raise PermissionDenied(
                "Only organization admins can create a knowledge item."
            )

        serializer.save()


class KnowledgeItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = KnowledgeItemSerializer
    permission_classes = [
        IsAuthenticated,
        IsKnowledgeItemOrganizationAdmin,
    ]

    def get_queryset(self):
        return KnowledgeItem.objects.filter(
            knowledge_base__moochat__organization__members__user=self.request.user
        )

    def perform_destroy(self, instance):
        delete_knowledge_item(instance)

        instance.delete()
