from django.core.management.base import BaseCommand

from mochats.models import KnowledgeItem
from mochats.rag import add_knowledge_item


class Command(BaseCommand):

    help = "Index all knowledge items into the vector store."

    def handle(self, *args, **options):

        knowledge_items = KnowledgeItem.objects.all()

        for knowledge_item in knowledge_items:
            add_knowledge_item(knowledge_item)

        self.stdout.write(self.style.SUCCESS("Knowledge items indexed successfully."))
