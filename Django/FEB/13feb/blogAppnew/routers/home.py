from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from core.config import templates

router = APIRouter()

@router.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    user_authenticated = "username" in request.session  
    username = request.session.get("username")  

    return templates.TemplateResponse("home.html", {
        "request": request,
        "user_authenticated": user_authenticated,
        "username": username
    })
