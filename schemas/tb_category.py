from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class tb_category(BaseModel):
    category_id: int
    name: str
    description: str

    class Config:
        orm_mode = True