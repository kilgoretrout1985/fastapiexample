from __future__ import annotations

import asyncio

import pytest


SAMPLE_DATA = {
    "sample_user": {"email": "test@localhost", "password": "pass"},
    "sample_user_2": {"email": "another@localhost", "password": "password"},
    "sample_item": {"title": "Nail", "description": "Also buy a hummer for your nails."},
    "sample_item_2": {"title": "Nail 2", "description": "Also buy a hummer 2 for your nails."},
}


@pytest.mark.asyncio
async def test_root(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.asyncio
async def test_create_user_ok(async_client):
    request_data = SAMPLE_DATA["sample_user"].copy()
    response = await async_client.post("/users/", json=request_data)
    assert response.status_code >= 200 and response.status_code < 300
    response_data = response.json()
    assert 'id' in response_data
    assert response_data['id'] > 0
    # substring in string for the case of trim
    assert response_data['email'] in request_data['email']
    assert 'password' not in response_data


@pytest.mark.asyncio
async def test_create_user_same_email(async_client):
    request_data = SAMPLE_DATA["sample_user"].copy()
    response1 = await async_client.post("/users/", json=request_data)
    response2 = await async_client.post("/users/", json=request_data)
    assert response1.status_code != response2.status_code  # 200 != 400
    assert response2.status_code == 400 or response1.status_code == 400


@pytest.mark.asyncio
async def test_create_user_not_enought_data(async_client):
    response = await async_client.post("/users/", json={"email": "not-enought-fields@localhost"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_read_users_empty(async_client):
    response = await async_client.get("/users/")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == []


@pytest.mark.asyncio
async def test_read_users_ok(async_client):
    await async_client.post("/users/", json=SAMPLE_DATA["sample_user"].copy())
    await async_client.post("/users/", json=SAMPLE_DATA["sample_user_2"].copy())
    response = await async_client.get("/users/")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 2


@pytest.mark.asyncio
async def test_read_specific_user_fail(async_client):
    response = await async_client.get("/users/-1")
    assert response.status_code >= 400
    response = await async_client.get("/users/IAmAStringThatWillFail")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_read_specific_user_ok(async_client):
    request_data = SAMPLE_DATA["sample_user"].copy()
    await async_client.post("/users/", json=request_data)
    response = await async_client.get("/users/1")
    assert response.status_code == 200
    response_data = response.json()
    del request_data['password']  # not returned in response
    assert dict(response_data, **request_data) == response_data


@pytest.mark.asyncio
async def test_create_user_item(async_client):
    request_user_data = SAMPLE_DATA["sample_user"].copy()
    request_item_data = SAMPLE_DATA["sample_item"].copy()
    user_id = (await async_client.post("/users/", json=request_user_data)).json()['id']
    assert user_id > 0

    post_url = f"/users/{user_id}/items/"

    response = await async_client.get(post_url)
    assert response.status_code == 405, "Get is not allowed to create an item"

    response = await async_client.post(post_url, json=request_item_data)
    response_data = response.json()
    assert response_data['owner_id'] == user_id
    assert dict(response_data, **request_item_data) == response_data

    response = await async_client.post(post_url, json={"description": "not enought fields posted"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_read_items(async_client):
    # gen data
    request_user_data = SAMPLE_DATA["sample_user"].copy()
    request_item_data = SAMPLE_DATA["sample_item"].copy()
    user_id = (await async_client.post("/users/", json=request_user_data)).json()['id']
    post_url = f"/users/{user_id}/items/"
    tasks = []
    for i in range(5):
        tasks.append(async_client.post(post_url, json=request_item_data))
    await asyncio.gather(*tasks)

    response = await async_client.get('/items/')
    assert len(response.json()) == 5
