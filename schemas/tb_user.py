from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    role_id: int
    name: str
    lastname: str
    msisdn: int
    email: EmailStr
    password: str
    
    class Config:
        orm_mode = True

class Login(BaseModel):
    email: EmailStr
    password: str