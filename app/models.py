from pydantic import BaseModel, Field
from typing import List, Optional

class RunRequest(BaseModel):
    documents: str = Field(..., description="Public URL to PDF / DOCX / email content")
    questions: List[str] = Field(..., description="List of natural language questions")

class SourcePassage(BaseModel):
    text: str
    page: Optional[int] = None
    score: Optional[float] = None

class AnswerItem(BaseModel):
    answer: str
    sources: List[SourcePassage]
    reasoning: Optional[str] = None

class RunResponse(BaseModel):
    answers: List[AnswerItem]
