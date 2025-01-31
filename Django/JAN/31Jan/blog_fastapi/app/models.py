import uuid
from sqlmodel import SQLModel, Field
from uuid import UUID

# Define the database model
class Blog(SQLModel, table=True):
    __tablename__ = "blog"
    
    # Define the columns in the blog table
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)  
    title: str = Field(index=True)  
    content: str