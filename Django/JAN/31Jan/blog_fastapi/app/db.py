from sqlmodel import create_engine, SQLModel
from sqlalchemy.orm import sessionmaker

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

# This function is used to create tables in the database
async def create_db_and_tables(app):
    # Create all tables in the database (if not already created)
    SQLModel.metadata.create_all(bind=engine)

    yield
