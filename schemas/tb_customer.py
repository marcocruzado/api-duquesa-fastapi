# Pydantic
from pydantic import BaseModel, Field, EmailStr

class Customer(BaseModel):
    name: str = Field(
        ...,
        min_length = 2,
        max_length = 255,
        title = "Name",
        description = "This is the customer's name. It's required.",
        example = "Pablo Perez"
        )
    phone: str = Field(
        ...,
        min_length = 10,
        max_length = 30,
        title = "Phone",
        description = "This is the phone. It's required.",
        example = "9999999999"
        )
    email: Optional[EmailStr] = Field(
        ...,
        title = "Email",
        description = "This is the email.",
        example = "customer@gmai.com"
        )
    status: int = Field(
        ...,
        gt = 0,
        le = 100,
        title = "Status",
        description = "Status",
        example = 1
        )