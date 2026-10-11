from langchain_chroma import Chroma

from .embeddings import get_embeddings


def get_vector_store():
    embeddings = get_embeddings()

    vector_store = Chroma(
        collection_name="moochat_knowledge",
        embedding_function=embeddings,
        persist_directory="chroma_db",
    )

    return vector_store
