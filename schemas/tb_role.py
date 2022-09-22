from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class tb_role(BaseModel):
    role_id: Optional[int]
    name: str
    
    class Config:
        orm_mode = True