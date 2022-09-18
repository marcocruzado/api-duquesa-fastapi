from datetime import datetime
from typing import List, Optional
from unicodedata import name
from pydantic import BaseModel

class tb_user(BaseModel):
    user_id: Optional[int]
    role_id: int
    name: str
    lastnames: str
    msisdn: str
    email: str
    password: str
    registration_timestamp: Optional[datetime]
    
    class Config:
        orm_mode = True