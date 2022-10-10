# Pydantic
from pydantic import BaseModel, Field

class Role(BaseModel):
    name: str = Field(
        ...,
        min_length = 4,
        max_length = 50,
        title = "Role name",
        description = "This is the role name. It's required.",
        example = "test"
        )