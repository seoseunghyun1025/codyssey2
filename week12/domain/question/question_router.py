# domain/question/question_router.py

import datetime  # datetime 임포트 추가
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status # status 임포트 추가

from database import get_db
from models import Question
from domain.question import question_schema

router = APIRouter(
    prefix="/api/question",
)

@router.get("/list", response_model=list[question_schema.Question])
def question_list(db: Session = Depends(get_db)):
    _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    return _question_list

# ---!!! question_create 함수가 추가되었습니다 !!!---
@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def question_create(_question_create: question_schema.QuestionCreate,
                    db: Session = Depends(get_db)):
    """
    POST 요청을 받아 새로운 질문을 생성하고 데이터베이스에 저장합니다.
    """
    # Question 모델 객체 생성
    new_question = Question(subject=_question_create.subject,
                            content=_question_create.content,
                            create_date=datetime.datetime.now())
    
    # 데이터베이스 세션에 추가
    db.add(new_question)
    
    # 데이터베이스에 커밋 (실제 저장)
    db.commit()