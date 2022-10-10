from pydantic import BaseModel, Field
from pydantic import EmailStr


class Login(BaseModel):
    email: EmailStr = Field(
        ...,
        title = "User email",
        description = "This is the user email. It's required.",
        example = " ashley@gmail.con",
        )
    password: str = Field(
        ...,
        min_length = 3,
        max_length = 255,
        title = "User password",
        description = "This is the user password. It's required.",
        example = "password"
        )