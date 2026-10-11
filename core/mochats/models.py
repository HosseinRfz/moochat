from django.conf import settings
from django.db import models

from organizations.models import Organization


class MooChat(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="moochats",
    )

    name = models.CharField(max_length=255)

    description = models.TextField(
        blank=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_moochats",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class KnowledgeBase(models.Model):
    moochat = models.ForeignKey(
        MooChat,
        on_delete=models.CASCADE,
        related_name="knowledge_bases",
    )

    name = models.CharField(max_length=255)

    description = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class KnowledgeItem(models.Model):

    class ItemType(models.TextChoices):
        TEXT = "TEXT", "Text"
        QA = "QA", "Q&A"

    knowledge_base = models.ForeignKey(
        KnowledgeBase,
        on_delete=models.CASCADE,
        related_name="items",
    )

    item_type = models.CharField(
        max_length=10,
        choices=ItemType.choices,
    )

    title = models.CharField(
        max_length=255,
        blank=True,
    )

    content = models.TextField(
        blank=True,
    )

    question = models.TextField(
        blank=True,
    )

    answer = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.title or f"KnowledgeItem #{self.id}"
