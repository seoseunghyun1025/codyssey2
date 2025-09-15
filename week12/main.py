# main.py

from fastapi import FastAPI
from domain.question import question_router

app = FastAPI()

# question_router.py 파일의 router 객체를 등록
app.include_router(question_router.router)