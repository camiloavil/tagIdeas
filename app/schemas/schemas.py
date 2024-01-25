from fastapi_users.schemas import BaseUser#, BaseUserCreate, BaseUserUpdate
from pydantic import BaseModel
from datetime import datetime
import uuid

class IdeaRead(BaseModel):
  id: uuid.UUID
  name: str
  content: str
  register_date:datetime

class IdeaRead_short(BaseModel):
  id: uuid.UUID
  name: str

class IdeaCreate(BaseModel):
  name: str
  content: str

class IdeaUpdate(BaseModel):
  name: str
  content: str

class UserRead(BaseUser[uuid.UUID]):
  first_name:str
  last_name:str
  photo_url:str
  register_date:datetime
  ideas: list[IdeaRead_short]
  # oauth_accounts: list

  def __init__(self, **data):
    ideas_ :list = data.pop('ideas')
    ideas :list[IdeaRead_short] = [IdeaRead_short(**idea.__dict__) for idea in ideas_]
    data['ideas'] = ideas
    super().__init__(**data)

# class UserCreate(BaseUserCreate):
#   pass

# class UserUpdate(BaseUserUpdate):
#   pass

