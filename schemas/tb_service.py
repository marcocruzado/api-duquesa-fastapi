# Pydantic
from pydantic import BaseModel, Field

class Service(BaseModel):
    category_id: int = Field(
        ...,
        gt = 0,
        le = 10000,
        example = 1003
        )
    name: str = Field(
        ...,
        min_length = 4,
        max_length = 50,
        example = "Limpieza e hidratación"
        )
    description: str = Field(
        ...,
        min_length = 10,
        max_length = 100,
        example = "Tratamientos faciales antiacné."
        )
    amount: float = Field(
        ...,
        gt = 0,
        le = 10000,
        example = 100
        )