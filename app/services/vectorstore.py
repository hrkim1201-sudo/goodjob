from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from app.services.embeddings import get_embeddings
from app.config import settings


def build_faiss_index(documents: list[Document]) -> FAISS:
    embeddings = get_embeddings()
    vector_store = FAISS.from_documents(documents, embeddings)
    vector_store.save_local(settings.FAISS_INDEX_DIR)
    return vector_store


def load_faiss_index() -> FAISS:
    index_dir = Path(settings.FAISS_INDEX_DIR)
    if not index_dir.exists():
        raise FileNotFoundError(f"FAISS 인덱스가 없습니다: {settings.FAISS_INDEX_DIR}")

    embeddings = get_embeddings()
    return FAISS.load_local(
        settings.FAISS_INDEX_DIR,
        embeddings,
        allow_dangerous_deserialization=True,
    )