from django.conf import settings

from langchain_google_genai import ChatGoogleGenerativeAI
from .prompts import conversation_prompt


def get_llm():
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0.7,
    )

    return llm


def generate_response(message):
    llm = get_llm()

    response = llm.invoke(message)

    return response.content


def generate_conversation_response(messages):
    llm = get_llm()

    from .rag import retrieve_relevant_documents

    last_user_message = messages[-1].content

    relevant_documents = retrieve_relevant_documents(
        last_user_message,
    )

    context = "\n\n".join(document.page_content for document in relevant_documents)

    prompt_messages = conversation_prompt.invoke(
        {
            "messages": messages,
            "context": context,
        }
    )

    response = llm.invoke(prompt_messages)

    if isinstance(response.content, list):
        return "".join(
            block["text"]
            for block in response.content
            if isinstance(block, dict) and block.get("type") == "text"
        )

    return response.content
