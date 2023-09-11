# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel, Field

class Additional(BaseModel):
    service_id: int = Field(
        ...,
        gt = 0,
        le = 1000000,
        title = "Service id",
        description = "This is the service id. It's required.",
        example = 5
        )
    name: str = Field(
        ...,
        min_length = 4,
        max_length = 50,
        title = "Name of the additional service",
        description = "This is the name of the additional service. It's required.",
        example = "Manicure PRO"
        )
    description: Optional[str] = Field(
        default = None,
        min_length = 2,
        max_length = 100,
        title = "Description of the additional service",
        description = "This is the description of the additional service. It's not required.",
        example = "Manicure profesional."
        )
    amount: float = Field(
        ...,
        gt = 0,
        le = 10000,
        title = "Amount of the additional service",
        description = "This is the amount of the additional service. It's required.",
        example = 50
        )