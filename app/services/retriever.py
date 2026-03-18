from app.services.vectorstore import load_faiss_index


def get_interview_retriever(k: int = 5):
    vector_store = load_faiss_index()
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": k, "fetch_k": 12},
    )
    return retriever


def build_retrieval_query(company_name: str, role_name: str, jd_text: str) -> str:
    # 너무 길면 retrieval 품질이 오히려 떨어질 수 있어 핵심 키워드 중심으로 구성
    jd_summary = jd_text[:500]
    return (
        f"기업명: {company_name}\n"
        f"직무: {role_name}\n"
        f"채용공고 핵심: {jd_summary}\n"
        f"관련 면접 질문, 기술 질문, 프로젝트 질문, 인성 질문"
    )