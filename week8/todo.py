# todo.py (업그레이드 버전)

import csv
import os
from typing import List, Dict
from fastapi import FastAPI, APIRouter, HTTPException
from model import TodoItem  # model.py에서 TodoItem 모델을 가져옵니다.

# --- FastAPI 앱 및 라우터 초기화 ---
# prefix를 사용해 이 라우터의 모든 경로 앞에 /todos를 붙입니다.
app = FastAPI()
router = APIRouter(prefix="/todos")

# --- 데이터 저장을 위한 CSV 파일 설정 ---
CSV_FILE = 'todolist.csv'
CSV_FIELDS = ['id', 'item']

# --- CSV 파일 관련 헬퍼 함수 (기존과 동일) ---
def read_todos_from_csv() -> List[Dict[str, str]]:
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, mode='r', encoding='utf-8', newline='') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

def write_todos_to_csv(todos: List[Dict[str, str]]):
    with open(CSV_FILE, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(todos)

# --- API 라우트 정의 ---

@router.get("/", summary='Retrieve the entire todo list')
def retrieve_todo() -> Dict[str, List[Dict[str, str]]]:
    """전체 할 일 리스트를 가져옵니다."""
    todo_list = read_todos_from_csv()
    return {"todo_list": todo_list}

@router.post("/", summary='Add a new todo item')
def add_todo(todo: TodoItem) -> Dict[str, str]:
    """새로운 할 일을 추가합니다."""
    todo_list = read_todos_from_csv()
    new_id = int(todo_list[-1]['id']) + 1 if todo_list else 1
    new_todo = {'id': str(new_id), 'item': todo.item}
    todo_list.append(new_todo)
    write_todos_to_csv(todo_list)
    return {'message': f"Todo '{todo.item}' added successfully with id {new_id}."}

@router.get("/{todo_id}", summary='Get a single todo item by its ID')
def get_single_todo(todo_id: int) -> Dict[str, str]:
    """ID를 사용해 특정 할 일 한 개를 조회합니다."""
    todo_list = read_todos_from_csv()
    for todo in todo_list:
        if int(todo['id']) == todo_id:
            return todo
    raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")

@router.put("/{todo_id}", summary='Update a todo item by its ID')
def update_todo(todo_id: int, todo_item: TodoItem) -> Dict[str, str]:
    """ID를 사용해 특정 할 일의 내용을 수정합니다."""
    todo_list = read_todos_from_csv()
    for index, todo in enumerate(todo_list):
        if int(todo['id']) == todo_id:
            todo_list[index]['item'] = todo_item.item
            write_todos_to_csv(todo_list)
            return {'message': f"Todo {todo_id} has been updated to '{todo_item.item}'."}
    raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")

@router.delete("/{todo_id}", summary='Delete a todo item by its ID')
def delete_single_todo(todo_id: int) -> Dict[str, str]:
    """ID를 사용해 특정 할 일을 삭제합니다."""
    todo_list = read_todos_from_csv()
    todo_to_delete = None
    for todo in todo_list:
        if int(todo['id']) == todo_id:
            todo_to_delete = todo
            break
    
    if todo_to_delete:
        todo_list.remove(todo_to_delete)
        write_todos_to_csv(todo_list)
        return {'message': f"Todo {todo_id} ('{todo_to_delete['item']}') has been deleted."}
    else:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")

# --- 라우터를 앱에 포함 ---
app.include_router(router)