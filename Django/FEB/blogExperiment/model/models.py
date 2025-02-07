from datetime import datetime, timezone
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True, nullable=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))

    blogs: List["Blog"] = Relationship(back_populates="author")
    comments: List["Comment"] = Relationship(back_populates="author")

class Blog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    author_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(tz=timezone.utc)}
    )

    author: User = Relationship(back_populates="blogs")
    comments: List["Comment"] = Relationship(back_populates="blog")

class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    author_id: int = Field(foreign_key="user.id")
    blog_id: int = Field(foreign_key="blog.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))

    author: User = Relationship(back_populates="comments")
    blog: Blog = Relationship(back_populates="comments")
