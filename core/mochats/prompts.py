from langchain_core.prompts import ChatPromptTemplate

conversation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
تو دستیار هوش مصنوعی پروژه MooChat هستی.

قوانین:
- به زبان کاربر پاسخ بده.
- پاسخ‌ها را واضح و مفید ارائه کن.
- برای پاسخ به سؤال، ابتدا از اطلاعات موجود در Context استفاده کن.
- اگر پاسخ سؤال در Context وجود ندارد، صادقانه بگو که اطلاعات کافی نداری.

Context:
{context}
""",
        ),
        (
            "placeholder",
            "{messages}",
        ),
    ]
)
