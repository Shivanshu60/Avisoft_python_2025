from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional




class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    blog_id: int = Field(foreign_key="blog.id")
    username: str  # the user who commented
    content: str
    # Relationship back to Blog
    blog: Optional["Blog"] = Relationship(back_populates="comments")