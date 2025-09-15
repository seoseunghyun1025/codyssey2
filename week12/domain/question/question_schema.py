# domain/question/question_schema.py

import datetime
from pydantic import BaseModel, validator

# ---!!! QuestionCreate 스키마가 추가되었습니다 !!!---
class QuestionCreate(BaseModel):
    subject: str
    content: str

    @validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime

    class Config:
        orm_mode = True