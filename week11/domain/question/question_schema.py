# domain/question/question_schema.py

import datetime
from pydantic import BaseModel

# 질문 목록 조회 시 사용할 Pydantic 모델
class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime

    # SQLAlchemy 모델과 Pydantic 모델을 연동하기 위한 설정
    class Config:
        orm_mode = True