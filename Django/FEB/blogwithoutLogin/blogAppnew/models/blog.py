from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.comment import Comment  # Import only for type hints

class Blog(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str
    body: str

    # all associated Comment objects are also deleted.
    comments: List["Comment"] = Relationship(
        back_populates="blog",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
