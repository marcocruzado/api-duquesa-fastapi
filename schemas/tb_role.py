# Pydantic
from pydantic import BaseModel, Field

class Role(BaseModel):
    name: str = Field(
        ...,
        min_length = 4,
        max_length = 50,
        example = "test"
        )