from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from model.models import *
from core.database import DBSession
from schema.schemas import UserLogin, UserCreate
from passlib.hash import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from utils import *



SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


router = APIRouter(prefix="/auth", tags=["Authentication"])

# Function to get current user from JWT token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  # 'sub' is where the username is stored
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    



@router.post("/login")
def login_user(session :DBSession, form_data: OAuth2PasswordRequestForm = Depends()):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    verified_password = verify_password(form_data.password, user.hashed_password)
    try:
        if not user or not verified_password:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Invalid username or password"
            )
    except Exception:
        print("An error occured")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token,
            "token_type": "bearer"}



@router.post("/register/")
def register_user(RegisterDetail: UserCreate, session :DBSession):
    existing_user = session.exec(select(User).where(User.username == RegisterDetail.username)).first()

    if existing_user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    hashed_password = get_password_hash(RegisterDetail.password)
    user = User(username = RegisterDetail.username, hashed_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "User registered Successfully"}






# SECRET_KEY = "secretsanta404"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# # Function to create access token
# def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
#     to_encode = data.copy()
#     expire = datetime.now(timezone.utc) + expires_delta  # Using timezone.utc
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# # def get_current_user(token: str = Depends(oauth2_scheme), session: DBSession = Depends(DBSession)):
# #     try:
# #         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
# #         username: str = payload.get("sub")  # 'sub' is the username
# #         if username is None:
# #             raise HTTPException(status_code=401, detail="Token is invalid")
        
# #         user = session.exec(select(User).where(User.username == username)).first()
# #         if user is None:
# #             raise HTTPException(status_code=404, detail="User not found")
        
# #         return user
# #     except JWTError:
# #         raise HTTPException(status_code=401, detail="Token is invalid")

# @router.post("/login/")
# def login(user: UserLogin, session: DBSession):
#     # Fetch user from the database by username
#     db_user = session.exec(select(User).where(User.username == user.username)).first()
    
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     # Verify password
#     if not bcrypt.verify(user.password, db_user.hashed_password):
#         raise HTTPException(status_code=401, detail="Incorrect password")
    
#     # Create access token
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(data={"sub": db_user.username}, expires_delta=access_token_expires)
    
#     return {"access_token": access_token, "token_type": "bearer"}




# @router.post("/register/")
# def register(user: UserCreate, session: DBSession):
#     existing_user = session.exec(select(User).where(User.email == user.email)).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     hashed_password = bcrypt.hash(user.password)
#     new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
#     session.add(new_user)
#     session.commit()
#     session.refresh(new_user)
#     return {"message": "User registered successfully", "user": new_user}



