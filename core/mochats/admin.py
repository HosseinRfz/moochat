from django.contrib import admin

from .models import MooChat, KnowledgeBase, KnowledgeItem


@admin.register(MooChat)
class MooChatAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "organization",
        "name",
        "created_at",
        "updated_at",
    ]

    search_fields = [
        "name",
        "organization__name",
    ]

    list_filter = [
        "created_at",
    ]


@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "moochat",
        "name",
        "created_at",
    ]

    search_fields = [
        "name",
        "moochat__name",
    ]

    list_filter = [
        "created_at",
    ]


@admin.register(KnowledgeItem)
class KnowledgeItemAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "knowledge_base",
        "item_type",
        "title",
        "created_at",
        "updated_at",
    ]

    search_fields = [
        "title",
        "content",
        "question",
        "answer",
    ]

    list_filter = [
        "item_type",
        "created_at",
    ]
