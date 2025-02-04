from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.comment import Comment  # Import only for type hints

class Blog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    body: str

    comments: List["Comment"] = Relationship(back_populates="blog")  # Use string reference
