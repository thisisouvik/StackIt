from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from bson import ObjectId
from app.database import db
from app.auth import get_current_user
from datetime import datetime

router = APIRouter()

class AnswerIn(BaseModel):
    question_id: str
    answer_text: str

@router.post("/answers")
async def post_answer(answer: AnswerIn, user: dict = Depends(get_current_user)):
    if not ObjectId.is_valid(answer.question_id):
        raise HTTPException(status_code=400, detail="Invalid question ID")

    question = await db.questions.find_one({"_id": ObjectId(answer.question_id)})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    data = {
        "question_id": ObjectId(answer.question_id),
        "user_id": user["email"],
        "answer_text": answer.answer_text,
        "created_at": datetime.utcnow()
    }
    result = await db.answers.insert_one(data)
    return {"msg": "Answer posted", "id": str(result.inserted_id)}

@router.get("/answers/{question_id}")
async def get_answers(question_id: str):
    answers = await db.answers.find({"question_id": ObjectId(question_id)}).to_list(100)
    return answers
