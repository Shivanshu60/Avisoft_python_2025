from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlmodel import select
from core.database import SessionDep
from models.blog import Blog
from core.config import templates

router = APIRouter()

@router.get("/create-blog/", response_class=HTMLResponse)
async def create_blog_page(request: Request):
    return templates.TemplateResponse("create-blog.html", {"request": request})

@router.post("/create-blog/")
async def create_blog(session: SessionDep, title: str = Form(...), body: str = Form(...)):
    blog = Blog(title=title, body=body)
    session.add(blog)
    session.commit()
    return RedirectResponse(url="/blogs", status_code=303)

@router.get("/blogs/", response_class=HTMLResponse)
async def read_blogs(request: Request, session: SessionDep):
    blogs = session.exec(select(Blog)).all()
    return templates.TemplateResponse("blogs.html", {"request": request, "blogs": blogs})

@router.post("/blog/{blog_id}")
async def delete_blog(blog_id: int, session: SessionDep):
    blog = session.get(Blog, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    session.delete(blog)
    session.commit()
    return RedirectResponse(url="/blogs", status_code=303)