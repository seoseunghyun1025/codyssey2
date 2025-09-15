# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite 데이터베이스 URL 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./board.db"

# 데이터베이스 엔진 생성
# connect_args는 SQLite 사용 시에만 필요한 설정입니다.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 데이터베이스 세션 생성
# autocommit=False: 데이터를 변경했을 때 자동으로 커밋하지 않음
# autoflush=False: 세션에 객체를 추가해도 즉시 DB에 반영하지 않음
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모델 클래스들이 상속받을 Base 클래스
Base = declarative_base()