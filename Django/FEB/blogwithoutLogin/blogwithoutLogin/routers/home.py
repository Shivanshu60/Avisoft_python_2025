from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from core.config import templates

router = APIRouter()

@router.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    username = request.session.get("username", "Guest")
    return templates.TemplateResponse("index.html", {"request": request, "username": username})
