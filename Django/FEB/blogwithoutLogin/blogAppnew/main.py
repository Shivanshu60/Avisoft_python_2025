from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.database import create_db_and_tables
from routers import home, blogs, auth
from models.blog import Blog
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

# Mount static files and include routers
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(home.router)
app.include_router(blogs.router)
app.include_router(auth.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()