import pytest
import asyncio
import httpx

from app.app import app
from app.db.db import Base, get_async_session

from fastapi import status
from typing import Callable, Awaitable, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


@pytest.fixture(scope="session")
def event_loop():
  """Force the pytest-asyncio loop to be the main one."""
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  yield loop
  loop.close()
  asyncio.set_event_loop(None)

# DATABASE_URL = "sqlite+aiosqlite:///./test.db"
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(DATABASE_URL)
Testing_async_session = async_sessionmaker(engine, expire_on_commit=False)

async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
  async with Testing_async_session() as session:
    yield session

async def create_db_and_tables():
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)

async def clean_db():
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="session")
async def init_db():
  """
  Fixture to initialize the database for a test session.
  """
  await create_db_and_tables()
  yield
  clean_db()

@pytest.fixture(scope="session")
async def client_db(init_db):
  """
  Fixture for creating a client database in the session scope.
  This function is asynchronous and yields a client for testing purposes.
  """
  print("client Started DB")
  app.dependency_overrides[get_async_session] = override_get_async_session
  async with httpx.AsyncClient(app=app, base_url="http://test.io") as client:
    yield client

@pytest.fixture(scope="session")
async def client():
  """
  Fixture for creating an async client for session scope.
  """
  print("simple client Started")
  async with httpx.AsyncClient(app=app, base_url="http://test.io") as client:
    yield client

# GetAuthenticatedAsyncClient = Callable[[dict], Awaitable[httpx.AsyncClient]]

# @pytest.fixture(scope="class")
# async def client_auth(client: httpx.AsyncClient)-> GetAuthenticatedAsyncClient:
#   print("start client_auth fixture")
#   async def _client_auth(user: dict) -> httpx.AsyncClient:
#     if 'id' not in user:
#       response_register = await client.post("/auth/register", json=user)
#       if response_register.status_code == status.HTTP_201_CREATED:
#         user.update(response_register.json())
#       elif response_register.status_code == status.HTTP_400_BAD_REQUEST:
#         raise Exception("Error registering user")
#     user_data = {
#       "username": user["email"],
#       "password": user["password"],
#     }
#     response = await client.post("/auth/jwt/login", data=user_data)
#     token = response.json()
#     client.headers["Authorization"] = f"Bearer {token['access_token']}"
#     return client
#   yield _client_auth
#   print("end client_auth fixture")
