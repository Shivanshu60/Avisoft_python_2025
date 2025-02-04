from fastapi import APIRouter, Request, Form, HTTPException, status, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from core.database import SessionDep
from models.user import User
from core.config import templates
from sqlmodel import select


router = APIRouter()

@router.get("/registration/", response_class=HTMLResponse)
async def registration(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/registration/")
async def registration(request: Request,session: SessionDep, username: str = Form(...), password: str = Form(...)):
    existing_user = session.exec(select(User).where(User.username == username)).first()
    
    if existing_user:
        return RedirectResponse(url="/registration?error=Username already exists", status_code=303)
    

    user = User(username=username, password=password)
    session.add(user)
    session.commit()

    request.session["username"] = user.username

    return RedirectResponse(url="/home", status_code=303)

@router.get("/login/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login/")
async def login(request: Request, session: SessionDep, username: str = Form(...), password: str = Form(...)):
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    
    if not user:
        return RedirectResponse(url="/login?error=User not found", status_code=303)
    
    if user.password != password:
        return RedirectResponse(url="/login?error=Incorrect password", status_code=303)

    # Store username in session
    request.session["username"] = user.username
    
    return RedirectResponse(url="/home", status_code=303)


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()  # Clear session data
    return RedirectResponse(url="/home", status_code=303)



    


