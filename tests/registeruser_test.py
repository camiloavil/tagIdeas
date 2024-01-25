import httpx
import pytest

from fastapi import status

"""
Tests the routes of "/auth/register" Users. Normally won't be used in production
"""

user1 = {
  "email": "pedrito@example.com",
  "password": "pepe123",
}
user2 = {
  "email": "pedrito_error@example.com"
}

@pytest.mark.asyncio
async def test_root(client: httpx.AsyncClient):
  response = await client.get("/")
  assert response.status_code == 200
  assert response.json() == {"message": "Hello!"}

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user,status_code",
    [
        (user1, status.HTTP_201_CREATED),
        (user1, status.HTTP_400_BAD_REQUEST),
        (user2, status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
async def test_register_users(client_db: httpx.AsyncClient, user: dict, status_code: status):
  response = await client_db.post("/auth/register", json=user)
  print(f"status code_recieved: {response.status_code}")
  print(response.json())
  assert response.status_code == status_code, "Response code not as expected"


# @pytest.fixture
# def user_login() -> dict[str, str | int]:
#     return user3

# @pytest.mark.asyncio
# async def test_getInfo_authenticatedUser(authenticated_client: httpx.AsyncClient, user_login: dict[str, str]):
#   response = await authenticated_client.get("/users/me")
#   user_get :dict = response.json()
#   del user_login["password"]
#   assert {(user_login[key] == user_get[key]) for key in user_login.keys()} == {True}
#   assert response.status_code == 200

