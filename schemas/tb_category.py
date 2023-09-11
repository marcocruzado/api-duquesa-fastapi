# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel, Field

class Category(BaseModel):
    name: str = Field(
        ...,
        min_length = 4,
        max_length = 50,
        title = "Category name",
        description = "This is the category name. It's required.",
        example = "Relajación"
        )
    description: Optional[str] = Field(
        default = None,
        min_length = 2,
        max_length = 100,
        title = "Category description",
        description = "This is the category description. It's not required.",
        example = "La mejor y mayor experiencia de relajación."
        )