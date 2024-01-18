from fastapi import FastAPI, Depends

from contextlib import asynccontextmanager

from app.config import get_settings
from app.middlewares import ErrorHandler
from app.db import User, create_db_and_tables
# from app.schemas import UserRead, UserCreate
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
async def authenticated_route(user: User = Depends(current_active_user)):
  return {"message": f"Hello {user.email}!"}

# @app.middleware("http")
# async def error_handler(request: Request, next_call: Callable):
#   try:
#     start_time = time.time()
#     response = await next_call(request)
#     process_time = time.time() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response
#   except Exception as e:
#     print(f"MAIN Error Handler Exception: {str(e)}")
#     return JSONResponse(status_code=500, content={'error': str(e)})
