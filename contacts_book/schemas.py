from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class ContactBase(BaseModel):
    firstname: str = Field(min_length=1, max_length=50)


class ContactModel(ContactBase):
    lastname: str = Field(max_length=50)
    email: EmailStr
    phone: str
    birthday: datetime
    description: str


class ContactResponce(ContactModel):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
