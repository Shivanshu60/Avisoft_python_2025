from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlmodel import select
from core.database import SessionDep
from models.blog import Blog
from models.comment import Comment
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
    blog = session.exec(select(Blog)).all()
    return templates.TemplateResponse(
        "allblogstitle.html",
        {
            "request": request,
            "blog": blog,
            "user_authenticated": user_authenticated,
            "username": username
        }
    )

@router.get("/blogs/{blog_id}", response_class=HTMLResponse)
async def blog_detail(
    request: Request,
    blog_id: int,  # Accept blog_id as a path parameter
    session: SessionDep,
    username: str | None = Depends(get_username)
):
    user_authenticated = username is not None

    # Query the database for the blog with the specified ID
    blog = session.exec(select(Blog).where(Blog.id == blog_id)).first()

    # If the blog is not found, raise a 404 error
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    comments = session.exec(select(Comment).where(Comment.blog_id == blog_id)).all()

    return templates.TemplateResponse(
        "blogDetails.html",
        {
            "request": request,
            "blog": blog,
            "comments": comments,
            "user_authenticated": user_authenticated,
            "username": username
        }
    )




@router.post("/blogs/{blog_id}/comment", response_class=HTMLResponse)
async def add_comment(
    request: Request,
    blog_id: int,
    session: SessionDep,
    comment_content: str = Form(...),  # Retrieve the comment content from the form
    username: str | None = Depends(get_username)
):
    # Ensure that the user is authenticated
    if username is None:
        raise HTTPException(status_code=401, detail="Authentication required to post comments")
    
    # Verify the blog exists
    blog = session.exec(select(Blog).where(Blog.id == blog_id)).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    # Create and save the new comment
    new_comment = Comment(blog_id=blog_id, username=username, content=comment_content)
    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)

    # Redirect back to the blog detail page after posting the comment
    return RedirectResponse(url=f"/blogs/{blog_id}", status_code=303)



@router.post("/blog/{blog_id}")
async def delete_blog(blog_id: int, session: SessionDep):
    blog = session.get(Blog, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    session.delete(blog)
    session.commit()
    return RedirectResponse(url="/blogs", status_code=303)