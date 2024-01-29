from fastapi_users.schemas import BaseUser, BaseUserCreate#, BaseUserUpdate
from pydantic import BaseModel, EmailStr
from datetime import datetime
import uuid

class taggedUser(BaseModel):
  email_tagged: EmailStr
  is_writeable: bool = False
  is_deleteable: bool = False

class taggedUserCreate(BaseModel):
  email_tagged: EmailStr
  is_writeable: bool = False
  is_deleteable: bool = False

class IdeaRead(BaseModel):
  id: uuid.UUID
  name: str
  content: str
  register_date:datetime
  tagged_user: list[taggedUser] = []

class IdeaRead_short(BaseModel):
  id: uuid.UUID
  name: str

class IdeaCreate(BaseModel):
  name: str
  content: str
  tagged_user: list[taggedUserCreate] = []

class IdeaUpdate(BaseModel):
  name: str
  content: str

class UserRead(BaseUser[uuid.UUID]):
  first_name:str
  last_name:str
  photo_url:str | None
  register_date:datetime
  ideas: list[IdeaRead_short]
  # oauth_accounts: list

  def __init__(self, **data):
    ideas_ :list = data.pop('ideas')
    ideas :list[IdeaRead_short] = [IdeaRead_short(**idea.__dict__) for idea in ideas_]
    data['ideas'] = ideas
    super().__init__(**data)

class UserCreate(BaseUserCreate):
  first_name:str
  last_name:str

# class UserUpdate(BaseUserUpdate):
#   pass

