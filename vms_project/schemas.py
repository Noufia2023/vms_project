from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    username : str
    email : str

class UserCreate(UserBase):
    password : str

class User(UserBase):
    created_dt : datetime

    class Config:
        orm_mode = True
    

