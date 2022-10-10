# Pydantic
from pydantic import BaseModel, Field
from pydantic import EmailStr

class User(BaseModel):
    role_id: int = Field(
        ...,
        gt = 0,
        le = 20,
        title = "Role id",
        description = "This is the role id. It's required.",
        example = 1
        )
    name: str = Field(
        ...,
        min_length = 4,
        max_length = 50,
        title = "User first names",
        description = "This is the user first names. It's required.",
        example = "Frank Bill"
        )
    lastname: str = Field(
        ...,
        min_length = 4,
        max_length = 50,
        title = "User last names",
        description = "This is the user last names. It's required.",
        example = "Palma Luna"
        )
    msisdn: int = Field(
        ...,
        gt = 7,
        le = 14,
        title = "User contact number",
        description = "This is the user contact number. It's required.",
        example = 933277769
        )
    email: EmailStr = Field(
        ...,
        title = "User email",
        description = "This is the user email. It's required.",
        example = "frank.palma@gmail.com"
        )
    password: str = Field(
        ...,
        min_length = 8,
        max_length = 255,
        title = "User password",
        description = "This is the user password. It's required.",
        example = "password"
        )