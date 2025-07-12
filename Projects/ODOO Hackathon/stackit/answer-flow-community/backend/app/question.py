from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.database import db
from app.auth import get_current_user
from datetime import datetime

router = APIRouter()

class QuestionIn(BaseModel):
    title: str
    body: str

@router.post("/questions")
async def post_question(question: QuestionIn, user: dict = Depends(get_current_user)):
    data = {
        "user_id": user["email"],
        "title": question.title,
        "body": question.body,
        "created_at": datetime.utcnow()
    }
    result = await db.questions.insert_one(data)
    return {"msg": "Question posted", "id": str(result.inserted_id)}

@router.get("/questions")
async def get_all_questions():
    questions = await db.questions.find().to_list(100)
    return questions
