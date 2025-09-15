# domain/question/question_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Question
from domain.question import question_schema

router = APIRouter(
    prefix="/api/question",
)

# 데이터베이스 세션을 가져오는 의존성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/list", response_model=list[question_schema.Question])
def question_list(db: Session = Depends(get_db)):
    """
    ORM을 사용하여 질문 목록을 조회합니다.
    """
    _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    return _question_list