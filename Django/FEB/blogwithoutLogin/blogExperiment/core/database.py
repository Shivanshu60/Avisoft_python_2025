from dotenv import load_dotenv
from sqlmodel import SQLModel, Session, create_engine
from typing import Annotated
from fastapi import Depends
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def initialize_db():
    """Creates the database and tables if they don't exist."""
    SQLModel.metadata.create_all(engine)

def get_db_session():
    """Yields a database session for dependency injection."""
    with Session(engine) as session:
        yield session

DBSession = Annotated[Session, Depends(get_db_session)]
