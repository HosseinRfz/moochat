from langchain_core.messages import HumanMessage, AIMessage

from .models import Conversation, Message

from mochats.services import (
    generate_conversation_response as generate_llm_response,
)


def get_conversation_messages(conversation):
    messages = []

    for message in conversation.messages.order_by("created_at"):

        if message.role == Message.Role.USER:
            messages.append(
                HumanMessage(
                    content=message.content,
                )
            )

        elif message.role == Message.Role.ASSISTANT:
            messages.append(
                AIMessage(
                    content=message.content,
                )
            )

    return messages


def generate_conversation_response(
    conversation,
    user_message,
):
    messages = get_conversation_messages(conversation)

    messages.append(
        HumanMessage(
            content=user_message,
        )
    )

    assistant_response = generate_llm_response(messages)

    Message.objects.create(
        conversation=conversation,
        role=Message.Role.USER,
        content=user_message,
    )

    assistant_message = Message.objects.create(
        conversation=conversation,
        role=Message.Role.ASSISTANT,
        content=assistant_response,
    )

    return assistant_message
