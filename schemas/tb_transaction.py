# Python
from typing import List
from typing import Optional

# Pydantic
from pydantic import BaseModel, Field

class Transaction(BaseModel):
    user_id: int = Field(
        ...,
        gt = 0,
        le = 1000000,
        title = "User id",
        description = "This is the user id. It's required.",
        example = 1
        )
    service_id: int = Field(
        ...,
        gt = 0,
        le = 1000000,
        title = "Service id",
        description = "This is the service id. It's required.",
        example = 1
        )
    additional_id: Optional[List[int]] = Field(
        default = None,
        gt = 0,
        le = 1000000,
        title = "Additional id",
        description = "This is the additional id. It's not required.",
        example = [1, 2]
        )
    service_amount: float = Field(
        ...,
        gt = 0,
        le = 10000,
        title = "Service amount",
        description = "This is the service amount. It's required.",
        example = 100
        )
    additional_amount:  Optional[List[int]]= Field(
        default = None,
        gt = 0,
        le = 10000,
        title = "Additional amount",
        description = "This is the additional amount. It's required.",
        example = [300, 500]
        )
    total_amount: float = Field(
        ...,
        gt = 0,
        le = 100000,
        title = "Total amount",
        description = "This is the total amount. It's required.",
        example = 900
        )