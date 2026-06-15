from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from app.database import db
from app.auth import hash_password, verify_password, create_access_token

router = APIRouter()

class UserIn(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    username: str
    email: EmailStr
    role: str

@router.post("/register")
async def register(user: UserIn):
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    user_dict = user.model_dump()
    user_dict["password_hash"] = hash_password(user_dict.pop("password"))
    user_dict["role"] = "user"
    await db.users.insert_one(user_dict)
    return {"msg": "User registered successfully"}

@router.post("/login")
async def login(user: UserIn):
    found = await db.users.find_one({"email": user.email})
    if not found or not verify_password(user.password, found["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": found["email"], "role": found["role"]})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/users")
async def get_users():
    users = await db.users.find().to_list(100)
    return [{"username": u["username"], "email": u["email"], "role": u["role"]} for u in users]
