from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from model.models import *
from core.database import SessionDep
from schema.schemas import CommentCreate


router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/")
def add_comment(comment: CommentCreate, session: SessionDep):
    blog = session.get(Blog, comment.blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    new_comment = Comment(content=comment.content, author_id=comment.author_id, blog_id=comment.blog_id)
    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)
    return new_comment

@router.delete("/{comment_id}")
def delete_comment(comment_id: int, session: SessionDep, user_id: int):
    comment = session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.author_id != user_id:
        raise HTTPException(status_code=403, detail="Permission denied")

    session.delete(comment)
    session.commit()
    return {"message": "Comment deleted"}
