from langchain_core.documents import Document

from .embeddings import get_embeddings
from .models import KnowledgeItem
from .vector_store import get_vector_store


def knowledge_item_to_document(item):
    if item.item_type == KnowledgeItem.ItemType.TEXT:
        content = item.content

    elif item.item_type == KnowledgeItem.ItemType.QA:
        content = f"Question: {item.question}\nAnswer: {item.answer}"

    else:
        content = ""

    return Document(
        page_content=content,
        metadata={
            "knowledge_item_id": item.id,
            "knowledge_base_id": item.knowledge_base_id,
            "moochat_id": item.knowledge_base.moochat_id,
            "item_type": item.item_type,
            "title": item.title,
        },
    )


def add_knowledge_item(item):
    vector_store = get_vector_store()

    document = knowledge_item_to_document(item)

    vector_store.add_documents(
        documents=[document],
        ids=[f"knowledge_item_{item.id}"],
    )


def retrieve_relevant_documents(query, moochat_id, k=4):
    vector_store = get_vector_store()

    documents = vector_store.similarity_search(
        query,
        k=k,
        filter={
            "moochat_id": moochat_id,
        },
    )

    return documents


def update_knowledge_item(item):
    vector_store = get_vector_store()

    document = knowledge_item_to_document(item)

    vector_store.update_documents(
        ids=[f"knowledge_item_{item.id}"],
        documents=[document],
    )


def delete_knowledge_item(item):
    vector_store = get_vector_store()

    vector_store.delete(
        ids=[f"knowledge_item_{item.id}"],
    )
