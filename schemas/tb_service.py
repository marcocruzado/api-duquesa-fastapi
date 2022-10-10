# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel, Field

class Service(BaseModel):
    category_id: int = Field(
        ...,
        gt = 0,
        le = 10000,
        title = "Category id",
        description = "This is the category id. It's required.",
        example = 1003
        )
    name: str = Field(
        ...,
        min_length = 4,
        max_length = 50,
        title = "Service name",
        description = "This is the service name. It's required.",
        example = "Limpieza e hidratación"
        )
    description: Optional[str] = Field(
        default = None,
        min_length = 10,
        max_length = 100,
        title = "Service description",
        description = "This is the service description. It's not required.",
        example = "Tratamientos faciales antiacné."
        )
    amount: float = Field(
        ...,
        gt = 0,
        le = 10000,
        title = "Service amount",
        description = "This is the service amount. It's required.",
        example = 100
        )