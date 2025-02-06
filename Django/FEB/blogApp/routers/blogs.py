from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlmodel import select
from core.database import SessionDep
from models.blog import Blog
from core.config import templates

router = APIRouter()

def get_username(request: Request) -> str | None:
    """Dependency to get the username from the session."""
    return request.session.get("username")

@router.get("/create-blog/", response_class=HTMLResponse)
async def create_blog_page(request: Request):
    # Check if the user is authenticated
    username = request.session.get("username")
    user_authenticated = username is not None
    
    if "username" not in request.session:
        return RedirectResponse(url="/login", status_code=303)
    
    return templates.TemplateResponse("create-blog.html", {"request": request,"user_authenticated": user_authenticated,"username": username})


@router.post("/create-blog/")
async def create_blog(request: Request, session: SessionDep, title: str = Form(...), body: str = Form(...)):
    # Check if authenticated
    if "username" not in request.session:
        return RedirectResponse(url="/login", status_code=303)  # Redirect to login if not authenticated

    username = request.session.get("username")
    

    blog = Blog(title=title, body=body)
    session.add(blog)
    session.commit()

    return RedirectResponse(url="/blogs", status_code=303)




@router.get("/blogs/", response_class=HTMLResponse)
async def read_blogs(request: Request, session: SessionDep, username: str | None = Depends(get_username)):
    user_authenticated = username is not None
    blogs = session.exec(select(Blog)).all()
    return templates.TemplateResponse(
        "blogs.html",
        {
            "request": request,
            "blogs": blogs,
            "user_authenticated": user_authenticated,
            "username": username
        }
    )


@router.post("/blog/{blog_id}")
async def delete_blog(blog_id: int, session: SessionDep):
    blog = session.get(Blog, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    session.delete(blog)
    session.commit()
    return RedirectResponse(url="/blogs", status_code=303)