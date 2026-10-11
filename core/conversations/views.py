from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Conversation, Message
from .permissions import IsConversationOwner, IsMessageConversationOwner
from .serializers import ConversationSerializer, MessageSerializer
from .services import generate_conversation_response


class ConversationListCreateView(generics.ListCreateAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ConversationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [
        IsAuthenticated,
        IsConversationOwner,
    ]

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(
            conversation_id=self.kwargs["conversation_id"],
            conversation__user=self.request.user,
        )

    def perform_create(self, serializer):
        conversation = get_object_or_404(
            Conversation,
            id=self.kwargs["conversation_id"],
            user=self.request.user,
        )

        assistant_message = generate_conversation_response(
            conversation=conversation,
            user_message=serializer.validated_data["content"],
        )

        serializer.instance = assistant_message


class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [
        IsAuthenticated,
        IsMessageConversationOwner,
    ]

    def get_queryset(self):
        return Message.objects.filter(conversation__user=self.request.user)
