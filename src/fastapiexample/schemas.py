from __future__ import annotations

from typing import Union

from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    title: str
    # check me working
    description: Union[str, None] = Field(default=None, title="Description of the item.", max_length=128)

    class Config:
        schema_extra = {
            "example": {
                "title": "Nail",
                "description": "Also buy a hummer for your nails.",
            }
        }


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


# for security, the password won't be in other Pydantic models,
# for example, it won't be sent from the API when reading a user
class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    # check me working
    items: list[Item] = []

    class Config:
        orm_mode = True
