from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    # email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class BlogCreate(BaseModel):
    title: str
    content: str
    author_id: int

class CommentCreate(BaseModel):
    content: str
    author_id: int
    blog_id: int
