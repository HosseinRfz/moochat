import logging

from django.db import transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import KnowledgeItem
from .rag import add_knowledge_item, delete_knowledge_item

logger = logging.getLogger(__name__)


def index_knowledge_item(item_id):
    try:
        item = KnowledgeItem.objects.get(pk=item_id)
        add_knowledge_item(item)
    except KnowledgeItem.DoesNotExist:
        return
    except Exception:
        logger.exception(
            "Failed to index KnowledgeItem %s",
            item_id,
        )


def remove_knowledge_item(item):
    try:
        delete_knowledge_item(item)
    except Exception:
        logger.exception(
            "Failed to delete KnowledgeItem %s from vector store",
            item.pk,
        )


@receiver(post_save, sender=KnowledgeItem)
def knowledge_item_saved(sender, instance, **kwargs):
    transaction.on_commit(
        lambda item_id=instance.pk: index_knowledge_item(item_id)
    )


@receiver(post_delete, sender=KnowledgeItem)
def knowledge_item_deleted(sender, instance, **kwargs):
    transaction.on_commit(
        lambda item=instance: remove_knowledge_item(item)
    )
