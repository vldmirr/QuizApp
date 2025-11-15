from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List, Optional


# Question Schemas
class QuestionBase(BaseModel):
    text: str = Field(..., min_length=1, max_length=800)

class QuestionCreate(QuestionBase):
    pass

class QuestionResponse(QuestionBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class QuestionWithAnswers(QuestionResponse):
    answers: List['AnswerResponse'] = []

# Answer Schemas
class AnswerBase(BaseModel):
    text: str = Field(..., min_length=1, max_length=800)
    user_id: str = Field(..., min_length=1, max_length=36)

class AnswerCreate(AnswerBase):
    pass

class AnswerResponse(AnswerBase):
    id: int
    question_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Update forward references
QuestionWithAnswers.model_rebuild()