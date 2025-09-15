# model.py

from pydantic import BaseModel

class TodoItem(BaseModel):
    """
    할 일(Todo) 항목의 데이터 모델입니다.
    - item: 할 일의 내용을 나타내는 문자열
    """
    item: str