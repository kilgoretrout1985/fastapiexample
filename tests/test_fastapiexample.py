from __future__ import annotations

import pytest


@pytest.mark.anyio
async def test_root(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.anyio
async def test_read_item(async_client):
    response = await async_client.get("/items/42")
    assert response.status_code == 200
    assert response.json() == {"item_id": 42}

    response = await async_client.get("/items/0")
    assert response.status_code == 200
    assert response.json() == {"item_id": 0}
