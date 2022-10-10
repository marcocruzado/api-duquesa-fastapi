from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr

class tb_user(BaseModel):
    user_id: Optional[int]
    role_id: int
    name: str
    lastname: str
    msisdn: str
    email: EmailStr
    password: str
    registration_timestamp: Optional[datetime]
    
    class Config:
        orm_mode = True

class Login(BaseModel):
    email: EmailStr
    password: str