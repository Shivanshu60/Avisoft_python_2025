from fastapi import FastAPI
from db import engine, create_db_and_tables

app = FastAPI(lifespan=create_db_and_tables)

