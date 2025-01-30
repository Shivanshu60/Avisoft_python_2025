from fastapi import FastAPI, Query, Form, File, UploadFile, HTTPException
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI()




class User(BaseModel):
    name:str
    password:str
    address:Optional[str]=None

@app.get("/")
def index(q: Optional[str]=Query(None, max_length=5, min_length=3, regex = "^shi")):  #validation v krskte h
    return {"q":q} 

@app.get("/items")
def index(q:Optional[List[str]]=Query([])):
    return {"q":q}
    

@app.post("/")
def index(user:User):
    return user.name


@app.get("/items/{item_id}")
def index(item_id: int):
    return{"product_id": item_id}

# @app.get("/items/")
# def index(q:int=0, m:Optional[int]=10):
#     return {"product is ": q,
#             "m":m,}

@app.get("/items/{file_path:path}")
def index(file_path:str):
    return {"file_path": file_path}

@app.post("/items/{user_id}")
def index(user_id:int, user:User):
    print(user_id)
    return user

# form data 
@app.post("/form/data")
async def form_data(username : str= Form(), password: str = Form()):
    return ({
        "username": username
    })


#file upload
@app.post("/file/upload")
async def file_bytes_len(file: bytes = File()):
    return({
        "file": len(file)
    })


@app.post("/file/upload/detail")
async def file_upload(file: UploadFile):
    return({
        "file": file
    })

items = [1,2,3,4,5]
@app.get("/error/handling")
async def error_handle (item: int):
    if item not in items:
        return HTTPException(status_code=400, detail=("Not in our list of items"))
    return {"value": item}





