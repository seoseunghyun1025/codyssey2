# todo.py

import csv
import os
from typing import List, Dict
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

# --- Pydantic 모델 정의 ---
# POST 요청 시 받을 데이터의 형식을 지정합니다.
class TodoItem(BaseModel):
    item: str

# --- FastAPI 앱 및 라우터 초기화 ---
app = FastAPI()
router = APIRouter()

# --- 데이터 저장을 위한 CSV 파일 설정 ---
CSV_FILE = 'todolist.csv'
CSV_FIELDS = ['id', 'item']

# --- CSV 파일 관련 헬퍼 함수 ---
def read_todos_from_csv() -> List[Dict[str, str]]:
    """CSV 파일에서 모든 할 일 목록을 읽어옵니다."""
    if not os.path.exists(CSV_FILE):
        return []
    
    with open(CSV_FILE, mode='r', encoding='utf-8', newline='') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

def write_todos_to_csv(todos: List[Dict[str, str]]):
    """할 일 목록 전체를 CSV 파일에 덮어씁니다."""
    with open(CSV_FILE, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(todos)

# --- API 라우트 정의 ---
@router.post("/add", summary='Add a new todo item')
def add_todo(todo: TodoItem) -> Dict[str, str]:
    """
    새로운 할 일을 리스트에 추가하고 CSV 파일에 저장합니다.
    - **item**: 추가할 할 일 내용 (JSON 형식)
    """
    todo_list = read_todos_from_csv()
    
    # 새 아이템의 ID 결정
    new_id = int(todo_list[-1]['id']) + 1 if todo_list else 1
    
    new_todo = {'id': str(new_id), 'item': todo.item}
    todo_list.append(new_todo)
    
    write_todos_to_csv(todo_list)
    
    return {'message': f"Todo '{todo.item}' added successfully."}

@router.get("/", summary='Retrieve the entire todo list')
def retrieve_todo() -> Dict[str, List[Dict[str, str]]]:
    """
    CSV 파일에 저장된 전체 할 일 리스트를 가져옵니다.
    """
    todo_list = read_todos_from_csv()
    return {"todo_list": todo_list}

# --- 라우터를 앱에 포함 ---
app.include_router(router)