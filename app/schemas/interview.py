from pydantic import BaseModel, Field
from typing import List, Literal


class InterviewQuestion(BaseModel):
    question_type: Literal["technical", "project", "behavioral", "company_fit"]
    question_text: str = Field(..., description="예상 면접 질문")
    reason: str = Field(..., description="이 질문이 생성된 이유")
    priority_score: float = Field(..., ge=0, le=10)


class InterviewQuestionSet(BaseModel):
    company_name: str
    role_name: str
    questions: List[InterviewQuestion]


class AnswerDraft(BaseModel):
    question_text: str
    answer_draft: str
    answer_strategy: str
    improvement_points: List[str]