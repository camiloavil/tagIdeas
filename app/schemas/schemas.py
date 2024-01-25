from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate
from pydantic import BaseModel
from datetime import datetime
import uuid

class UserRead(BaseUser[uuid.UUID]):
  first_name:str
  last_name:str
  photo_url:str
  register_date:datetime
  # check only the number of items
  # oauth_accounts: list
class UserCreate(BaseUserCreate):
  pass

class UserUpdate(BaseUserUpdate):
  pass

class IdeaRead(BaseModel):
  id: uuid.UUID
  name: str
  content: str
  register_date:datetime

class IdeaCreate(BaseModel):
  name: str
  content: str

class IdeaUpdate(BaseModel):
  name: str
  content: str
