from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship
from fastapi_users.db import (SQLAlchemyBaseOAuthAccountTableUUID,
                              SQLAlchemyBaseUserTableUUID,
                              # SQLAlchemyUserDatabase
                            )

from .MySQLAlchemyUserDatabase import MySQLAlchemyUserDatabase

DATABASE_URL = "sqlite+aiosqlite:///./myDB.db"

class Base(DeclarativeBase):
  pass

class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
  pass

class User(SQLAlchemyBaseUserTableUUID, Base):
  oauth_accounts: Mapped[list[OAuthAccount]] = relationship(
    "OAuthAccount", lazy="joined"
  )

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
