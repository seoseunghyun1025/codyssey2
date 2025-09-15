# models.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False, default=datetime.datetime.now)

    # Answer 모델과의 관계 설정
    answers = relationship("Answer", backref="question", cascade="all, delete-orphan")

class Answer(Base):
    __tablename__ = 'answer'

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False, default=datetime.datetime.now)

    # Question 모델과의 외래 키 관계 설정
    question_id = Column(Integer, ForeignKey("question.id"))