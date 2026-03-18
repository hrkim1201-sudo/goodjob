from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.services.vectorstore import build_faiss_index


DATA_DIR = Path("./data/interview_corpus")


def load_text_documents() -> list[Document]:
    docs: list[Document] = []

    for file_path in DATA_DIR.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")
        docs.append(
            Document(
                page_content=text,
                metadata={
                    "source": str(file_path),
                    "filename": file_path.name,
                },
            )
        )
    return docs


def chunk_documents(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
    )
    return splitter.split_documents(documents)


def run_ingest() -> None:
    raw_docs = load_text_documents()
    chunked_docs = chunk_documents(raw_docs)
    build_faiss_index(chunked_docs)
    print(f"인덱싱 완료: {len(chunked_docs)}개 청크")