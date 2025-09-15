# create_data.py
from database import SessionLocal
from models import Question
import datetime

db = SessionLocal()

# 데이터가 이미 있는지 확인
if db.query(Question).count() == 0:
    q1 = Question(subject='화성에서 식물 재배가 가능할까요?', content='감자를 심어보고 싶습니다.', create_date=datetime.datetime.now())
    q2 = Question(subject='지구 귀환 캡슐 설계 문의', content='현재 제안된 설계안의 안정성에 대해 논의하고 싶습니다.', create_date=datetime.datetime.now())
    db.add(q1)
    db.add(q2)
    db.commit()
    print("샘플 데이터가 성공적으로 생성되었습니다.")
else:
    print("데이터가 이미 존재합니다. 생성을 건너뜁니다.")

db.close()