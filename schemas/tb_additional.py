from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class tb_additional(BaseModel):
    additional_id: Optional[int]
    service_id: int
    name: str
    description: str
    amount: float
    registration_timestamp: Optional[datetime]

    class Config:
        orm_mode = True