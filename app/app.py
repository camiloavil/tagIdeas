from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
import time

from contextlib import asynccontextmanager
from typing import Callable
from app.db import User, create_db_and_tables
from app.schemas import UserCreate, UserRead, UserUpdate
from app.users import (
    SECRET,
    auth_backend,
    current_active_user,
    fastapi_users,
    google_oauth_client,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
    print("Shutting down FastAPI Server")

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
app.include_router(
    fastapi_users.get_oauth_router(google_oauth_client, auth_backend, SECRET),
    prefix="/auth/google",
    tags=["auth"],
)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@app.middleware("http")
async def error_handler(request: Request, next_call: Callable):
  try:
    start_time = time.time()
    response = await next_call(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
  except Exception as e:
    print(f"MAIN Error Handler Exception: {str(e)}")
    return JSONResponse(status_code=500, content={'error': str(e)})