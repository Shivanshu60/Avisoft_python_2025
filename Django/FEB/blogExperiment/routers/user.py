from fastapi import APIRouter, Depends
from sqlmodel import select
from model.models import *
from core.database import SessionDep

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
def get_users(session: SessionDep):
    users = session.exec(select(User)).all()
    return users

@router.get("/{user_id}")
def get_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        return {"error": "User not found"}
    return user
