from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class tb_category(BaseModel):
    category_id: Optional[int]
    name: str
    description: str

    class Config:
        orm_mode = True