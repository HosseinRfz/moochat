from django.conf import settings
from langchain_cohere import CohereEmbeddings


def get_embeddings():
    embeddings = CohereEmbeddings(
        model="embed-multilingual-v3.0",
        cohere_api_key=settings.COHERE_API_KEY,
    )
    return embeddings
