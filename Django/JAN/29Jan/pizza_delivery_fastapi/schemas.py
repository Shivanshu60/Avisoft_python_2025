from pydantic import BaseModel
from typing import Optional


class SignUpModel(BaseModel):
    id: Optional[int]
    username:str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        orm_model = True
        json_schema_extra = {
            'example': {
                "username":"johndoe",
                "email": "johndoe@gmail.com",
                "is_staff": False,
                "is_active": True
            }
        }