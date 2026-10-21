from rest_framework import serializers

from .models import MooChat
from .models import KnowledgeBase
from .models import KnowledgeItem


class MooChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = MooChat
        fields = [
            "id",
            "organization",
            "name",
            "description",
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


class KnowledgeBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = KnowledgeBase
        fields = [
            "id",
            "moochat",
            "name",
            "description",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]


class KnowledgeItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = KnowledgeItem
        fields = [
            "id",
            "knowledge_base",
            "item_type",
            "title",
            "content",
            "question",
            "answer",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        item_type = attrs.get(
            "item_type",
            getattr(self.instance, "item_type", None),
        )

        content = attrs.get(
            "content",
            getattr(self.instance, "content", ""),
        )

        question = attrs.get(
            "question",
            getattr(self.instance, "question", ""),
        )

        answer = attrs.get(
            "answer",
            getattr(self.instance, "answer", ""),
        )

        if item_type == KnowledgeItem.ItemType.TEXT:

            if not content:
                raise serializers.ValidationError(
                    {"content": "Content is required for TEXT items."}
                )

            if question or answer:
                raise serializers.ValidationError(
                    {
                        "question": (
                            "Question and answer are not allowed " "for TEXT items."
                        )
                    }
                )

        elif item_type == KnowledgeItem.ItemType.QA:

            if not question:
                raise serializers.ValidationError(
                    {"question": "Question is required for Q&A items."}
                )

            if not answer:
                raise serializers.ValidationError(
                    {"answer": "Answer is required for Q&A items."}
                )

            if content:
                raise serializers.ValidationError(
                    {"content": "Content is not allowed for Q&A items."}
                )

        return attrs
