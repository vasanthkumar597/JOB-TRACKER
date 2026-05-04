from fastapi import APIRouter, HTTPException
from database import SessionLocal
from models import User
from schemas import UserSchema
from auth import create_token
from fastapi import APIRouter
import models 
from passlib.hash import bcrypt




router = APIRouter()



@router.post("/register")
def register(user: UserSchema):
    db = SessionLocal()

    hashed_password = bcrypt.hash(user.password)

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role="user")
    

    db.add(new_user)
    db.commit()

    return {"message": "User created"}


@router.post("/login")
def login(user: UserSchema):
    db = SessionLocal()

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Wrong password")

    token = create_token({"sub": db_user.email})

    print("TOKEN GENERATED:", token)

    return {"access_token": token}
    

