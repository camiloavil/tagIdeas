import httpx
import pytest

from fastapi import status

"""
Tests the routes of "/auth/register" Users. Normally won't be used in production
"""

user1 = {
  "first_name": "Pedro",
  "last_name": "Carrizo",
  "email": "pedrito@example.com",
  "password": "pepe123",
}
user2 = {
  "email": "pedrito_error@example.com"
}
user3 = {
  "first_name": "Maria",
  "last_name": "Lotel",
  "email": "maria_lotel@example.com",
  "password": "maria123",
}

idea1 = {
  "name": "Idea 1",
  "content": "Idea 1 content"
}
idea2 = {
  "name": "Idea 2",
  "content": "Idea 2 content",
  "tagged_user": [{
    "email_tagged": "pedrito@example.com",
  }]
}
idea3 = {
  "name": "Idea 3",
  "content": "Idea 3 content",
  "tagged_user": [{
    "email_tagged": "pedrito@example.com",
  },{
    "email_tagged": "maria_lotel@example.com",
    "is_writeable": True
  }]
}
idea4 = {
  "name": "Idea 4",
  "content": "Idea 4 content"
}

@pytest.fixture
def user_login() -> dict[str, str]:
  return user3

@pytest.fixture()
async def authenticated_client(client_db: httpx.AsyncClient, user_login: dict[str, str]) -> httpx.AsyncClient:
  print("Setting Authenticated Client")
  login = {"username": user_login["email"], "password": user_login["password"]}
  response = await client_db.post("/auth/jwt/login", data = login)
  token :dict[str, any] = response.json()
  # print(token)
  client_db.headers["Authorization"] = f"Bearer {token['access_token']}"
  yield client_db

@pytest.mark.asyncio
async def test_root(client: httpx.AsyncClient):
  """
  Asynchronous test function for the root endpoint.

  Args:
    client (httpx.AsyncClient): The HTTP client for making asynchronous requests.

  Returns:
    None
  """
  response = await client.get("/")
  assert response.status_code == 200
  assert response.json() == {"message": "Hello!"}

@pytest.mark.asyncio
@pytest.mark.parametrize(
  "user,status_code",
  [
    (user1, status.HTTP_201_CREATED),
    (user2, status.HTTP_422_UNPROCESSABLE_ENTITY),
    (user1, status.HTTP_400_BAD_REQUEST),
    (user3, status.HTTP_201_CREATED),
  ],
)
async def test_register_users(client_db: httpx.AsyncClient, user: dict, status_code: status):
  """
  Asynchronous test function for registering users.
  Parameters:
    - client_db: An httpx.AsyncClient for making async HTTP requests.
    - user: A dictionary representing the user to be registered.
    - status_code: An HTTP status code to be expected in the response.

  Returns:
    - None
  """
  response = await client_db.post("/auth/register", json=user)
  print(f"status code_recieved: {response.status_code}")
  print(response.json())
  assert response.status_code == status_code, "Response code not as expected"

@pytest.mark.asyncio
async def test_getInfo_authenticatedUser(authenticated_client: httpx.AsyncClient, user_login: dict[str, str]):
  response = await authenticated_client.get("/mydata")
  user = user_login.copy()
  del user["password"]
  user_get :dict[str, any] = response.json()
  assert response.status_code == 200
  assert {(user_login[key] == user_get[key]) for key in user.keys()} == {True}
  assert len(user_get["ideas"]) == 0

@pytest.mark.asyncio
@pytest.mark.parametrize(
  "idea,status_code,msj",
  [
    (idea1, status.HTTP_201_CREATED, "add Idea 1"),
    (idea2, status.HTTP_201_CREATED, "add Idea 2"),
    (idea3, status.HTTP_201_CREATED, "add Idea 3"),
    (idea4, status.HTTP_201_CREATED, "add Idea 4"),
    (idea1, status.HTTP_409_CONFLICT, "Idea's name must be unique"),
  ],
)
async def test_SetIdeas(authenticated_client: httpx.AsyncClient, idea: dict[str, str], status_code: status, msj: str):
  response = await authenticated_client.post("/mydata/idea" , json = idea)
  print(response.json())
  assert response.status_code == status_code, msj
  if status_code == status.HTTP_201_CREATED:
    idea_get :dict[str, any] = response.json()
    assert all(idea_get[key] == idea[key] for key in idea.keys() if key != "tagged_user") is True, "Data should be the same"
    print(f"Checking this idea: {idea_get['name']}")
  if 'tagged_user' in idea:
    print("Idea has tagged users.")
    tags_ : list[dict[str, str]] = idea["tagged_user"]
    tags_get : list[dict[str, str]] = idea_get["tagged_user"]
    assert len(tags_get) == len(tags_)

@pytest.mark.asyncio
async def test_GetIdeas(authenticated_client: httpx.AsyncClient):
  """
  Test the GetIdeas function with an authenticated client, checking various scenarios of CRUD
  such as getting ideas, modifying them, and deleting them, and asserting the
  responses and data structure.
  """
  response = await authenticated_client.get("/mydata/idea")
  assert response.status_code == 200
  assert isinstance(response.json(), list), "Response is not a list"
  user_ideas :list[dict[str, str]] = response.json()
  assert len(user_ideas) == 4, "The number of ideas is not 4"
  items = ('id', 'name', 'content','register_date','tagged_user')
  for idea_got in user_ideas:
    assert all(key in idea_got for key in items), "Some keys are missing"
  ##### Test get idea by id
  idea_test = user_ideas[0].copy()
  response = await authenticated_client.get("/mydata/idea", params={"id": idea_test['id']})
  assert response.status_code == 200, "Response code not as expected"
  idea_get :dict[str, any] = response.json()
  assert all(idea_get[key] == idea_test[key] for key in idea_test.keys()) is True, "Data should be the same"
  ###Test modify idea by id
  idea_test["name"] = "Idea 1 modified name"
  idea_test["content"] = "Idea 1 modified content"
  ###Test send Idea whitout id
  response = await authenticated_client.put("/mydata/idea", json = idea_test)
  assert response.status_code == status.HTTP_404_NOT_FOUND, "Response code not as expected"
  response = await authenticated_client.put("/mydata/idea", json = idea_test, params={"id": idea_test['id']})
  idea_get :dict[str, any] = response.json()
  ###Test the idea modified must be the same
  assert all(idea_get[key] == idea_test[key] for key in idea_test.keys()) is True, "Data should be the same"
  ### Delete whit wrong id
  wrong_id = idea_test['id'].replace('1', '2').replace('2', '3').replace('3', '4').replace('4', '5')
  print(f"Test Delete idea wrong id -> {wrong_id}")
  response = await authenticated_client.delete("/mydata/idea", params={"id": wrong_id})
  assert response.status_code == status.HTTP_404_NOT_FOUND, "Response code not as expected"
  ### Delete whit right id
  print(f"Test Delete idea right id -> {wrong_id}")
  response = await authenticated_client.delete("/mydata/idea", params={"id": idea_test['id']})
  assert response.status_code == status.HTTP_200_OK, "Response code not as expected"
  ### Test get idea deleted must be blank
  response = await authenticated_client.get("/mydata/idea", params={"id": idea_test['id']})
  print(response.json())
  assert response.status_code == status.HTTP_404_NOT_FOUND
