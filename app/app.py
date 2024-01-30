from contextlib import asynccontextmanager
from fastapi import FastAPI, status, Depends
from fastapi.responses import JSONResponse
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.ideas import crudDB
from app.db import User, Idea, create_db_and_tables, get_async_session
# from app.db import User, create_db_and_tables
from app.middlewares import ErrorHandler
from app.config import get_settings
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
  tags=["OAuth"],
)

app.include_router(
  fastapi_users.get_register_router(schemas.UserRead, schemas.UserCreate),
  prefix="/auth",
  tags=["Auth"],
)
app.include_router(
  fastapi_users.get_auth_router(auth_backend),
  prefix="/auth/jwt",
  tags=["Auth"]
)

@app.get("/")
async def root():
  return {"message": "Hello!"}

@app.get("/mydata",
  response_model = schemas.UserRead,
  status_code=status.HTTP_200_OK
  )
async def mydata(user: User = Depends(current_active_user),
) -> schemas.UserRead:
  userfb = crudDB.get_user_info_db(user)
  return userfb

@app.post(path="/mydata/idea",
  response_model = schemas.IdeaRead,
  status_code = status.HTTP_201_CREATED
)
async def post_Idea(idea: schemas.IdeaCreate,
  user: User = Depends(current_active_user),
  session_db: AsyncSession = Depends(get_async_session)
) -> schemas.IdeaRead:
  try:
    return await crudDB.set_idea_db(session_db, user, idea)
  except crudDB.DuplicateIdeaName:
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"message": f"Idea's '{idea.name}'name already exists"})
  except Exception as e:
    print(f"Idea not created. Exception: {str(e)}")
    return JSONResponse(status_code=500, content={"message": "internal server error. Idea not created"})

@app.get("/mydata/idea",
  response_model = schemas.IdeaRead | list[schemas.IdeaRead],
  status_code = status.HTTP_200_OK
)
async def getIdeas(id: uuid.UUID | None = None,
  user: User = Depends(current_active_user),
) -> schemas.IdeaRead | list[schemas.IdeaRead]:
  if id:
    idea = crudDB.get_idea_db(user, id)
    if idea:
      return idea
    return JSONResponse(status_code=404, content={"message": "Idea not found"})
  return crudDB.get_ideas_db(user)

@app.put("/mydata/idea",
  response_model = schemas.IdeaRead,
  status_code = status.HTTP_202_ACCEPTED
)
async def updateIdea(
  new_idea : schemas.IdeaUpdate,
  id: uuid.UUID = None,
  user: User = Depends(current_active_user),
  session_db: AsyncSession = Depends(get_async_session)
) -> schemas.IdeaRead:
  print(f"Update idea by id -> {id}")
  if not id:
    return JSONResponse(status_code=404, content={"message": "Idea not found"})
  idea = await crudDB.update_idea_db(session_db, user, new_idea, id)
  if idea:
    return idea
  else:
    return JSONResponse(status_code=404, content={"message": "Idea not found"})

@app.delete("/mydata/idea",
  status_code = status.HTTP_200_OK,
  response_class = JSONResponse
)
async def deleteIdea(id: uuid.UUID = None,
  user: User = Depends(current_active_user),
  session_db: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
  if await crudDB.delete_idea_db(session_db, user, id):
    return JSONResponse(status_code=200, content = {"message": "Idea deleted"})
  else:
    return JSONResponse(status_code=404, content={"message": "Idea not found"})

