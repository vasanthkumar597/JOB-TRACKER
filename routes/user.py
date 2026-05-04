from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal
from models import User
from schemas import UserResponse
from auth import get_current_user

router = APIRouter()




@router.delete("/user/{user_id}")
def delete_user(user_id:int,current_user=Depends(get_current_user)):
    db=SessionLocal()

    db_user=db.query(User).filter(User.id==user_id).first()

    if not db_user.email!=current_user:
        raise HTTPException(status_code=404,detail="Not allowed")
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()

    return { "message":"User deleted successfully"}

@router.get("/users", response_model=list[UserResponse])
def get_users(user=Depends(get_current_user)):
    db = SessionLocal()
    return db.query(User).all()


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, user=Depends(get_current_user)):
    db = SessionLocal()

    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


