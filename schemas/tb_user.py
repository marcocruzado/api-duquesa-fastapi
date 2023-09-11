# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    role_id: int = Field(
        ...,
        gt = 0,
        le = 100,
        title = "Role id",
        description = "This is the role id. It's required.",
        example = 2
        )
    name: str = Field(
        ...,
        min_length = 2,
        max_length = 255,
        title = "Name",
        description = "This is the user name. It's required.",
        example = "Gianluca"
        )
    lastname: str = Field(
        ...,
        min_length = 2,
        max_length = 255,
        title = "Last name",
        description = "This is the user's last name. It's required.",
        example = "Lapadula Vargas",
        )
    msisdn: str = Field(
        ...,
        min_length = 10,
        max_length = 30,
        title = "Msisdn",
        description = "This is the msisdn. It's required.",
        example = "9999999999"
        )
    email: EmailStr = Field(
        ...,
        title = "Email",
        description = "This is the email. It's required.",
        example = "gianluca.lapadula@hotmail.com"
        )
    password: Optional[str] = Field(
        ...,
        title = "Password",
        description = "This is the password.",
        example = "password"
        )
    status: int = Field(
        ...,
        gt = -1,
        le = 10000,
        title = "Status",
        description = "This is the status. It's required.",
        example = 1
        )

class Login(BaseModel):
    email: EmailStr = Field(
        ...,
        title = "Email",
        description = "This is the email. It's required.",
        example = "gianluca.lapadula@hotmail.com"
        )
    password: str = Field(
        ...,
        min_length = 5,
        max_length = 50,
        title = "Password",
        description = "This is the password. It's required.",
        example = "password"
        )