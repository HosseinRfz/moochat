from rest_framework import serializers

from .models import Conversation, Message


class ConversationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conversation
        fields = [
            "id",
            "moochat",
            "user",
            "title",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
        ]


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = [
            "id",
            "conversation",
            "role",
            "content",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "conversation",
            "role",
            "created_at",
        ]
