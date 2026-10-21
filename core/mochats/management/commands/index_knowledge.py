from django.core.management.base import BaseCommand

from mochats.models import KnowledgeItem
from mochats.vector_store import get_vector_store
from mochats.rag import add_knowledge_item


class Command(BaseCommand):

    help = "Rebuild the vector store from current knowledge items."

    def handle(self, *args, **options):
        vector_store = get_vector_store()

        vector_store.delete_collection()

        knowledge_items = KnowledgeItem.objects.all()

        for knowledge_item in knowledge_items:
            add_knowledge_item(knowledge_item)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully indexed {knowledge_items.count()} knowledge items."
            )
        )
