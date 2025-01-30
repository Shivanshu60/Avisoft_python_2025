from fastapi import FastAPI, Depends, HTTPException
from typing import List

from sqlalchemy.orm import session
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

