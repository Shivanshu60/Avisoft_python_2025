from fastapi import FastAPI
from unittest.util import _MAX_LENGTH
from enum import Enum
from typing import Union
from pydantic import BaseModel


app = FastAPI()

class Choice_Names(str, Enum):
    one = "one"
    two = "two"
    three = "three"


@app.get("/")
async def root():
    return {"message": "I am Shivanshu"}

@app.get("/shivanshu")
async def shivanshu():
    return {"message": "This is another route shivanshu !"}

@app.get("item/{Item}")
def path_func(Item):
    var_name = {"path variable": Item}
    return (var_name)

@app.get("/query")
def query_func(name: str, roll_no: int):
    var_name = {"name": name, "roll no": roll_no}
    return (var_name)

@app.get("/models/{model_name}")
async def get_model(model_name: Choice_Names):
    if model_name.value == "one":
        return {"model_name": model_name, "message": "Calling One!!!"}
    if model_name.value == "two":
        return {"model_name": model_name, "message": "Calling two!!!"}

    return {"model_name": model_name, "message": "have some"}


@app.get("/query")
def query_func(name: Union[str, None] = None, roll_n: Union[str, None] = Query(default=None, min_length=3, max_length=3)):
    var_name = {"name": name, "roll no": roll_no}
    return {var_name}
    

