from datetime import datetime
from typing import List, Optional
from unicodedata import category
from pydantic import BaseModel


class tb_service(BaseModel):
    service_id: Optional[int]
    category_id: int
    name: str
    description: str
    amount: float
    registration_timestamp: Optional[datetime]

    class Config:
        orm_mode = True