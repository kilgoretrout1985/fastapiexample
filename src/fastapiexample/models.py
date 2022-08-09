from __future__ import annotations

from typing import Union

from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str
    description: Union[str, None] = Field(default=None, title="Description of the item.", max_length=128)
    price: float = Field(gt=0, description="Price must be greater than zero.")
    tax: Union[float, None] = Field(ge=0)  # can be either null or non-negative
