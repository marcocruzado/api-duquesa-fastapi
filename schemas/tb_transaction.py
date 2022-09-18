from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class tb_transaction(BaseModel):
    transaction_id: Optional[int]
    user_id: int
    service_id: int
    service_amount: float
    additional_amount: List[int]
    total_amount: float
    registration_timestamp: Optional[datetime]

    class Config:
        orm_mode = True