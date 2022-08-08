from __future__ import annotations

from fastapi import FastAPI, Path

from fastapiexample.models import Item


app = FastAPI()


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int = Path(ge=1)):
    return {"item_id": item_id}


@app.post("/items/")
async def create_item(item: Item):
    return item
