from pathlib import Path
from langchain_core.prompts import PromptTemplate
from app.services.embeddings import get_llm
from app.schemas.interview import AnswerDraft
from app.schemas.user_profile import UserProfile
from app.services.question_chain import format_user_profile


PROMPT_PATH = Path("./app/prompts/answer_prompt.txt")


def generate_answer_draft(
    question_text: str,
    job_description: str,
    user: UserProfile,
) -> AnswerDraft:
    prompt_text = PROMPT_PATH.read_text(encoding="utf-8")
    prompt = PromptTemplate.from_template(prompt_text)

    llm = get_llm(temperature=0.3)
    structured_llm = llm.with_structured_output(AnswerDraft)

    chain = prompt | structured_llm

    result = chain.invoke(
        {
            "question_text": question_text,
            "job_description": job_description,
            "user_profile": format_user_profile(user),
        }
    )

    result.question_text = question_text
    return result