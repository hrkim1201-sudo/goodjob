from pydantic import BaseModel
from typing import List


class Project(BaseModel):
    title: str
    description: str
    role: str
    tech_stack: List[str]
    achievements: List[str]


class UserProfile(BaseModel):
    name: str
    desired_role: str
    skills: List[str]
    projects: List[Project]
    portfolio_summary: str