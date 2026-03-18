from pathlib import Path
from langchain_core.prompts import PromptTemplate
from app.services.embeddings import get_llm
from app.services.retriever import get_interview_retriever, build_retrieval_query
from app.schemas.interview import InterviewQuestionSet
from app.schemas.user_profile import UserProfile


PROMPT_PATH = Path("./app/prompts/question_prompt.txt")


def format_user_profile(user: UserProfile) -> str:
    project_lines = []
    for p in user.projects:
        project_lines.append(
            f"- 프로젝트명: {p.title}\n"
            f"  역할: {p.role}\n"
            f"  기술스택: {', '.join(p.tech_stack)}\n"
            f"  설명: {p.description}\n"
            f"  성과: {', '.join(p.achievements)}"
        )

    return (
        f"이름: {user.name}\n"
        f"희망직무: {user.desired_role}\n"
        f"보유기술: {', '.join(user.skills)}\n"
        f"포트폴리오 요약: {user.portfolio_summary}\n"
        f"프로젝트:\n" + "\n".join(project_lines)
    )


def generate_interview_questions(
    company_name: str,
    role_name: str,
    job_description: str,
    user: UserProfile,
) -> InterviewQuestionSet:
    retriever = get_interview_retriever(k=6)
    retrieval_query = build_retrieval_query(company_name, role_name, job_description)
    docs = retriever.invoke(retrieval_query)

    retrieved_context = "\n\n".join(
        [f"[출처: {doc.metadata.get('filename', 'unknown')}]\n{doc.page_content}" for doc in docs]
    )

    prompt_text = PROMPT_PATH.read_text(encoding="utf-8")
    prompt = PromptTemplate.from_template(prompt_text)

    llm = get_llm(temperature=0.2)

    structured_llm = llm.with_structured_output(InterviewQuestionSet)

    chain = prompt | structured_llm

    result = chain.invoke(
        {
            "job_description": job_description,
            "user_profile": format_user_profile(user),
            "retrieved_context": retrieved_context,
        }
    )

    # 스키마에 company/role이 비어 나올 수 있으므로 보정
    result.company_name = company_name
    result.role_name = role_name
    return result