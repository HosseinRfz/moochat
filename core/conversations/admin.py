from django.contrib import admin

from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "moochat",
        "user",
        "title",
        "created_at",
        "updated_at",
    ]

    search_fields = [
        "title",
        "user__username",
    ]

    list_filter = [
        "moochat",
        "created_at",
    ]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "conversation",
        "role",
        "created_at",
    ]

    search_fields = [
        "content",
    ]

    list_filter = [
        "role",
        "created_at",
    ]
