from fastapi import FastAPI, Path, Query, Form, File, UploadFile, HTTPException
from unittest.util import _MAX_LENGTH
from enum import Enum
from typing import Union
from pydantic import BaseModel

class schema1(BaseModel):
    name: str
    Class: str
    roll_no: int

app = FastAPI()

class Choice_Names(str, Enum):
    one = "one"
    two = "two"
    three = "three"


@app.get("/hello")
async def root():
    return {"msg":"Hello World"}

@app.get("/item/{item}")
def path_func(item):
    return {"msg":item}

@app.get("/query")
def path_func(name: Union[str, None]= None, roll_no: Union[int, None]= Query(default=None,
min_length=3, max_length=5)):
    var_name = {"name": name, "roll no": roll_no}
    return (var_name)

@app.get("/models/{model_name}")
async def get_model(model_name: Choice_Names):
    if model_name.value == "one":
        return {"model_name": model_name, "message": "calling one"}

    if model_name.value == "two":
        return {"model_name": model_name, "message": "calling two"}

    if model_name.value == "three":
        return {"model_name": model_name, "message": "calling three"}



# request body
@app.post("/items/")
async def create_item(item: schema1):
    return item

class vipan(BaseModel):
    one:str
    two: str
    three: int


# form data 
@app.post('/form/data')
# async def form_data(username: str = Form(), password: str = Form()):
async def form_data(items: vipan):
    return ({"items": items})
    # return ({"username": username}, {"password": password})
     

    
# file upload
@app.post("/file/upload")
async def file_bytes_len(file: bytes = File()):
    return ({"file": len(file)})

    
@app.post("/upload/file")
async def file_upload(file: UploadFile):
    return ({"file_name": file.filename, "file_content_name": file.content_type})

items = [1,2,3,4,5]

# error handling 
@app.get("/error/handling")
async def handle_error(item: int):
    if item not in items:
        return HTTPException(status_code = 400, detail= "Item not in list (1,2,3,4,5)")
    return {"value": item}