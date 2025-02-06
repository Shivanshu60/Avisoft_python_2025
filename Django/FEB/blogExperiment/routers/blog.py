from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import select
from model.models import *
from core.database import DBSession
from schema.schemas import BlogCreate
from fastapi.responses import HTMLResponse
from core.config import templates


router = APIRouter(prefix="/blogs", tags=["Blogs"])

@router.get("/home", response_class=HTMLResponse)
def get_blogs(request: Request):
    # check if user is authenticated or not 
    
    return templates.TemplateResponse("home.html", {
        "request": request,

    })

@router.get("/all", response_class=HTMLResponse)
def get_blogs(request: Request, session: DBSession):
    # check if user is authenticated or not 

    blog = session.exec(select(Blog)).all()
    
    return templates.TemplateResponse(
        "allblogstitle.html", {
        "request": request,

    })

# @router.post("/home")
# def create_blog(blog: BlogCreate, session: SessionDep):
#     new_blog = Blog(title=blog.title, content=blog.content, author_id=blog.author_id)
#     session.add(new_blog)
#     session.commit()
#     session.refresh(new_blog)
#     return new_blog


# @router.delete("/{blog_id}")
# def delete_blog(blog_id: int, session: SessionDep, user_id: int):
#     blog = session.get(Blog, blog_id)
#     if not blog:
#         raise HTTPException(status_code=404, detail="Blog not found")

#     if blog.author_id != user_id:
#         raise HTTPException(status_code=403, detail="Permission denied")

#     session.delete(blog)
#     session.commit()
#     return {"message": "Blog deleted"}
