from __future__ import annotations

from typing import Any, Union

from fastapi import FastAPI, Path

from fastapiexample.models import Item
from fastapiexample.middleware import add_custom_header_middleware


app = FastAPI()

app.middleware("http")(add_custom_header_middleware)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}


@app.get("/items/{item_id}", tags=['items'])
async def read_item(item_id: int = Path(ge=1)):
    return {"item_id": item_id}


@app.put("/items/{item_id}", tags=['items'])
async def update_item(item_id: int = Path(ge=1), item: Union[Item, None] = None) -> dict[str, Any]:
    results: dict[str, Any] = {"item_id": item_id}
    if item:
        results["item"] = item.dict()
    return results


@app.post("/items/", tags=['items'])
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    """
    return item
