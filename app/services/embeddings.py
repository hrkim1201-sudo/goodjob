from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from app.config import settings


def get_embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        model=settings.EMBEDDING_MODEL,
        api_key=settings.OPENAI_API_KEY,
    )


def get_llm(temperature: float = 0.2) -> ChatOpenAI:
    return ChatOpenAI(
        model=settings.MODEL_NAME,
        temperature=temperature,
        api_key=settings.OPENAI_API_KEY,
    )