from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from typing import Dict, Any, cast
import httpx

from app.config import get_settings
from app.middlewares import ErrorHandler
from app.db import User, OAuthAccount, create_db_and_tables, get_async_session
# from app.schemas import UserRead, UserCreate
from app.users import (
  SECRET,
  auth_backend,
  current_active_user,
  fastapi_users,
  google_oauth_client,
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

@asynccontextmanager
async def lifespan(app: FastAPI):
  await create_db_and_tables()
  yield
  # print("Shutting down FastAPI Server")

app = FastAPI(lifespan=lifespan)
app.title = get_settings().app_name

app.add_middleware(ErrorHandler)

app.include_router(
  fastapi_users.get_oauth_router(oauth_client = google_oauth_client,
                                 backend = auth_backend,
                                 state_secret = SECRET,
                                 associate_by_email = True,
                                 is_verified_by_default = True,
                                 ),
  prefix="/auth/google",
  tags=["auth"],
)

@app.get("/")
async def root():
  return {"message": "Hello!"}

@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user), session_db: AsyncSession = Depends(get_async_session)):
  print(user.id)
  statement = (
    select(OAuthAccount)
    .where(OAuthAccount.oauth_name == google_oauth_client.name)
    .where(OAuthAccount.account_id == user.id)
  )
  print(statement)
  OAuthData = await session_db.execute(statement)
  print(OAuthData)
  print(type(OAuthData))
  return {"message": f"Hello {user.email}!"}

@app.get("/testing")
async def testingOAuth(user: User = Depends(current_active_user)) -> Dict[str, Any]:
    print(f"{user.email} - {user.id}")
    print(f'get token of google {user.getOAuthToken("google")}')

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://people.googleapis.com/v1/people/me",
            params={"personFields": "names,photos"},
            headers={"Accept": "application/json",
                     "Authorization": f"Bearer {user.getOAuthToken('google')}"},
        )
    data = cast(Dict[str, Any], response.json())
    print(data)
    first_name, last_name = next(
        (name.get('givenName'), name.get('familyName')) #displayName
        for name in data["names"]
        if name["metadata"]["primary"]
    )
    photo_url = next(
        photo["url"] for photo in data["photos"] if photo["metadata"]["primary"]
    )

    return {"first_name": first_name, "last_name": last_name, "photo_url": photo_url}

