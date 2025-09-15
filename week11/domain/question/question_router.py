# domain/question/question_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# ---!!! 수정된 import 부분 !!!---
from database import get_db  # database.py에서 get_db를 직접 가져옵니다.
from models import Question
from domain.question import question_schema

router = APIRouter(
    prefix="/api/question",
)

# 라우터 내에 있던 get_db 함수는 이제 필요 없으므로 삭제합니다.

@router.get("/list", response_model=list[question_schema.Question])
def question_list(db: Session = Depends(get_db)):
    """
    ORM을 사용하여 질문 목록을 조회합니다.
    Depends(get_db)를 통해 요청마다 새로운 DB 세션을 받고,
    요청이 끝나면 자동으로 세션이 반환됩니다.
    """
    _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    return _question_list