# database.py

import contextlib
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./board.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ---!!! 여기가 추가/수정된 부분입니다 !!!---
@contextlib.contextmanager
def get_db():
    """
    contextlib.contextmanager를 사용하여 데이터베이스 세션을 관리하는
    의존성 함수입니다.
    요청이 시작될 때 세션을 생성하고, 끝나면 자동으로 닫습니다.
    """
    db = SessionLocal()
    try:
        yield db  # API 함수에 db 세션 객체를 전달합니다.
    finally:
        db.close() # API 함수의 처리가 끝나면 세션을 닫습니다.