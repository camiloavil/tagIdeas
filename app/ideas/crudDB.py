from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
import uuid

from app.db import User, Idea#, get_async_session
from app import schemas


class DuplicateIdeaName(Exception):
  def __init__(self, message="Idea's name already exists"):
    self.message = message
    super().__init__(self.message)

def get_user_info_db(user: User) -> schemas.UserRead:
  userfb = schemas.UserRead(**user.__dict__)
  return userfb

async def set_idea_db(
  session_db: AsyncSession,
  user : User,
  idea: schemas.IdeaCreate,
) -> schemas.IdeaRead:
  print("Testing save Idea")
  print(idea)
  name = next((idea_db.name for idea_db in user.ideas if idea_db.name == idea.name), None)
  print(name)
  if name:
    raise DuplicateIdeaName(f"Idea's name '{idea.name}' already exists")

  idea_db = Idea(**idea.model_dump())
  session_db.add(idea_db)
  user.ideas.append(idea_db)
  session_db.add(user)
  try:
    await session_db.commit()
    await session_db.refresh(idea_db)
  except Exception as e:
    print(f"Idea not created. Exception: {str(e)}")
    raise Exception("Idea not created")
  return schemas.IdeaRead(**idea_db.__dict__)

def get_idea_db(
  user: User,
  id: uuid.UUID
) -> schemas.IdeaRead | None:
  print(f"Get idea by id -> {id}")
  idea = next((idea for idea in user.ideas if idea.id == id), None)
  if idea:
    return schemas.IdeaRead(**idea.__dict__)
  return None

def get_ideas_db(user : User) -> list[schemas.IdeaRead]:
  print(f"Get all ideas of {user.email}")
  ideas : list[schemas.IdeaRead] = [schemas.IdeaRead(**idea.__dict__) for idea in user.ideas]

  print("Test")
  for idea in user.ideas:
    print(idea.__dict__)
  return ideas

async def update_idea_db(
  session_db: AsyncSession,
  user: User,
  new_idea : schemas.IdeaUpdate,
  id: uuid.UUID = None,
)-> schemas.IdeaRead | None:
  idea = next((idea for idea in user.ideas if idea.id == id), None)
  if idea:
    idea.name = new_idea.name
    idea.content = new_idea.content
    session_db.add(idea)
    try:
      await session_db.commit()
      await session_db.refresh(idea)
    except Exception as e:
      print(f"Idea not updated. Exception: {str(e)}")
    return schemas.IdeaRead(**idea.__dict__)
  else:
    return None

async def delete_idea_db(
  session_db: AsyncSession,
  user: User,
  id: uuid.UUID,
)-> bool:
  idea = next((idea for idea in user.ideas if idea.id == id), None)
  if idea:
    try:
      await session_db.delete(idea)
      await session_db.commit()
    except Exception as e:
      print(f"Idea not deleted. Exception: {str(e)}")
    return True
  return False
