from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from model.models import *
from core.database import SessionDep
from schema.schemas import BlogCreate


router = APIRouter(prefix="/blogs", tags=["Blogs"])

@router.post("/")
def create_blog(blog: BlogCreate, session: SessionDep):
    new_blog = Blog(title=blog.title, content=blog.content, author_id=blog.author_id)
    session.add(new_blog)
    session.commit()
    session.refresh(new_blog)
    return new_blog

@router.get("/")
def get_blogs(session: SessionDep):
    return session.exec(select(Blog)).all()

@router.delete("/{blog_id}")
def delete_blog(blog_id: int, session: SessionDep, user_id: int):
    blog = session.get(Blog, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    if blog.author_id != user_id:
        raise HTTPException(status_code=403, detail="Permission denied")

    session.delete(blog)
    session.commit()
    return {"message": "Blog deleted"}
