from fastapi import APIRouter
from pydantic import BaseModel
from app.schemas.user_profile import UserProfile
from app.services.question_chain import generate_interview_questions
from app.services.answer_chain import generate_answer_draft


router = APIRouter(prefix="/api/v1/interviews", tags=["interviews"])


class QuestionGenerateRequest(BaseModel):
    company_name: str
    role_name: str
    job_description: str
    user_profile: UserProfile


class AnswerGenerateRequest(BaseModel):
    question_text: str
    job_description: str
    user_profile: UserProfile


@router.post("/questions/generate")
def generate_questions(req: QuestionGenerateRequest):
    result = generate_interview_questions(
        company_name=req.company_name,
        role_name=req.role_name,
        job_description=req.job_description,
        user=req.user_profile,
    )
    return result.model_dump()


@router.post("/answers/generate")
def generate_answer(req: AnswerGenerateRequest):
    result = generate_answer_draft(
        question_text=req.question_text,
        job_description=req.job_description,
        user=req.user_profile,
    )
    return result.model_dump()