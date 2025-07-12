from fastapi import FastAPI
from app import users, question, answer

app = FastAPI()

app.include_router(users.router)
app.include_router(question.router)
app.include_router(answer.router)
