from typing import AsyncGenerator, TYPE_CHECKING
from datetime import datetime
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship
from fastapi_users.db import (SQLAlchemyBaseOAuthAccountTableUUID,
                              SQLAlchemyBaseUserTableUUID,
                              # SQLAlchemyUserDatabase
                            )

from .MySQLAlchemyUserDatabase import MySQLAlchemyUserDatabase, MySQLAlchemyIdeaTableUUID
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, DateTime

DATABASE_URL = "sqlite+aiosqlite:///./myDB.db"

class Base(DeclarativeBase):
  pass

class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
  pass

class Idea(MySQLAlchemyIdeaTableUUID, Base):
  pass

class User(SQLAlchemyBaseUserTableUUID, Base):
  if TYPE_CHECKING:  # pragma: no cover
    first_name:str
    last_name:str
    photo_url:str
    register_date:datetime
  else:
    first_name: Mapped[str] = mapped_column(String(length=100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(length=100), index=True, nullable=True)
    photo_url: Mapped[str] = mapped_column(String(length=1000), unique=True, nullable=True)
    register_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

  ideas: Mapped[list[Idea]] = relationship("Idea", lazy="joined")
  oauth_accounts: Mapped[list[OAuthAccount]] = relationship(
    "OAuthAccount", lazy="joined"
  )

  def __repr__(self) -> str:
    return f"User(id={self.id!r},name={self.first_name!r} {self.last_name!r}, email={self.email!r})"

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
