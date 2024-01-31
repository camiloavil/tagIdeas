from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship
from fastapi_users.db import SQLAlchemyBaseOAuthAccountTableUUID

from .MySQLAlchemyUserDatabase import (
  MySQLAlchemyUserDatabase,
  MySQLAlchemyIdeaTableUUID,
  MySQLAlchemyBaseUserTableUUID,
  MySQLAlchemyTaggedUserTableUUID
  )

DATABASE_URL = "sqlite+aiosqlite:///./myDB.db"

class Base(DeclarativeBase):
  pass

class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
  pass

class TaggedUser(MySQLAlchemyTaggedUserTableUUID, Base):
  pass

class Idea(MySQLAlchemyIdeaTableUUID, Base):
  tagged_user: Mapped[list[TaggedUser]] = relationship(
    "TaggedUser", lazy="joined"
    )
  def __repr__(self) -> str:
    truncated_content = (self.content[:10] + '...') if len(self.content) > 10 else self.content
    return f"Idea(id={self.id!r}, name={self.name!r}, content={truncated_content!r})"

class User(MySQLAlchemyBaseUserTableUUID, Base):
  ideas: Mapped[list[Idea]] = relationship(
    "Idea", lazy="joined"
    )
  oauth_accounts: Mapped[list[OAuthAccount]] = relationship(
    "OAuthAccount", lazy="joined"
  )
  def __repr__(self) -> str:
    return f"User(id={self.id!r},name={self.first_name!r} {self.last_name!r}, email={self.email!r}), N_ideas={len(self.ideas)}"

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def create_db_and_tables():
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
  async with async_session_maker() as session:
    yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
  """
  Asynchronous function to get the user database using the provided session.
  It takes an AsyncSession object as a parameter and yields a MySQLAlchemyUserDatabase
  object containing User and OAuthAccount.
  MySQLAlchemyUserDatabase is a subversion of SQLAlchemyUserDatabase.
  """
  yield MySQLAlchemyUserDatabase(session, User, OAuthAccount)

#Original piece of code: It works
# async def get_user_db(session: AsyncSession = Depends(get_async_session)):
#   yield SQLAlchemyUserDatabase(session, User, OAuthAccount)
