from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any, cast
import httpx

from app.db import User, Idea, create_db_and_tables, get_async_session
from app.middlewares import ErrorHandler
from app.config import get_settings
# from app.schemas import UserRead, UserCreate
from app import schemas
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
  tags=["OAuth"],
)

@app.get("/")
async def root():
  return {"message": "Hello!"}

@app.get("/mydata")
async def mydata(user: User = Depends(current_active_user),
  session_db: AsyncSession = Depends(get_async_session)
) -> schemas.UserRead:
  print(f"user DB model __dict__ method: {user.__dict__}")
  print(f"user DB model __repr__ method: {user}")
  userfb = schemas.UserRead(**user.__dict__)
  print("user fb")
  print(userfb)
  return userfb

@app.post("/mydata/idea")
async def post_Idea(idea: schemas.IdeaCreate,
  user: User = Depends(current_active_user),
  session_db: AsyncSession = Depends(get_async_session)
) -> schemas.IdeaRead:
  idea_db = Idea(**idea.model_dump())
  session_db.add(idea_db)
  user.ideas.append(idea_db)
  session_db.add(user)
  await session_db.commit()
  await session_db.refresh(idea_db)
  print(idea_db.__dict__)
  return schemas.IdeaRead(**idea_db.__dict__)
  return {"message": f"'{idea.name}' Idea was created by {user.email}!"}

@app.get("/mydata/idea")
async def getIdeas(user: User = Depends(current_active_user),
  # session_db: AsyncSession = Depends(get_async_session)
) -> list[schemas.IdeaRead]:
  print(user)
  ideas : list[schemas.IdeaRead] = []
  ideas = [schemas.IdeaRead(**idea.__dict__) for idea in user.ideas]
  return ideas

@app.get("/mydata/idea/{id}")
async def getIdea(id: str, user: User = Depends(current_active_user),
) -> schemas.IdeaRead:
  idea = next((idea for idea in user.ideas if idea.id == id), None)
  if idea:
    return schemas.IdeaRead(**idea.__dict__)
  else:
    return JSONResponse(status_code=404, content={"message": "Idea not found"})

@app.put("/mydata/idea/{id}")
async def updateIdea(id: str,
  idea : schemas.IdeaUpdate,
  user: User = Depends(current_active_user),
  session_db: AsyncSession = Depends(get_async_session)
) -> schemas.IdeaRead:
  idea = next((idea for idea in user.ideas if idea.id == id), None)
  if idea:
    idea.content = "new content"
    session_db.add(idea)
    await session_db.commit()
    await session_db.refresh(idea)
    return schemas.IdeaRead(**idea.__dict__)
  else:
    return JSONResponse(status_code=404, content={"message": "Idea not found"})

@app.delete("/mydata/idea/{id}")
async def deleteIdea(id: str,
  user: User = Depends(current_active_user),
  session_db: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
  idea = next((idea for idea in user.ideas if idea.id == id), None)
  if idea:
    session_db.delete(idea)
    await session_db.commit()
    return JSONResponse(status_code=200, content = {"message": "Idea deleted"})
  else:
    return JSONResponse(status_code=404, content={"message": "Idea not found"})

@app.get("/testing")
async def testingOAuth(user: User = Depends(current_active_user)) -> Dict[str, Any]:
  print(f"{user.email} - {user.id}")
  return {"testing" : (user.first_name+" "+user.last_name)}

