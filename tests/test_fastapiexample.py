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
    assert response.status_code == 422

    response = await async_client.get("/items/IAmAStringThatWillFail")
    assert response.status_code == 422


@pytest.mark.anyio
async def test_create_item(async_client):
    # get is not allowed on creation
    response = await async_client.get("/items/")
    assert response.status_code == 405

    request_data_1 = {"name": "Lol", "price": 42.1}
    response = await async_client.post("/items/", json=request_data_1)
    assert response.status_code == 200
    response_data = response.json()
    # because of None as a default value we check here that
    # request_data_1 is actually a sub-dict of response_data
    assert dict(response_data, **request_data_1) == response_data

    # tax is int here, will it be autoconverted to float???
    request_data_2 = {"name": "Lol", "price": 42.1, "tax": 2, "description": "Some desc"}
    response = await async_client.post("/items/", json=request_data_2)
    assert response.status_code == 200
    assert response.json() == request_data_2  # all fields used here, so == is enought

    response = await async_client.post("/items/", json={"name": "not enought fields posted"})
    assert response.status_code == 422


@pytest.mark.anyio
async def test_update_item(async_client):
    response = await async_client.put("/items/42")
    assert response.status_code == 200
    assert 'item_id' in response.json()
    assert response.json()['item_id'] == 42

    request_data = {'name': 'test', 'price': 55.5}
    response = await async_client.put("/items/42", json=request_data)
    assert response.status_code == 200
    response_data = response.json()
    assert 'item' in response_data
    assert dict(response_data['item'], **request_data) == response_data['item']
