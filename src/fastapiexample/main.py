from __future__ import annotations

from typing import Any, Union

from fastapi import FastAPI, Path

from fastapiexample.models import Item


app = FastAPI()


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int = Path(ge=1)):
    return {"item_id": item_id}


@app.put("/items/{item_id}")
async def update_item(item_id: int = Path(ge=1), item: Union[Item, None] = None) -> dict[str, Any]:
    results: dict[str, Any] = {"item_id": item_id}
    if item:
        results["item"] = item.dict()
    return results


@app.post("/items/")
async def create_item(item: Item):
    return item
