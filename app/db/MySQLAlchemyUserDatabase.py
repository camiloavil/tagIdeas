import uuid
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseOAuthAccountTable
from sqlalchemy import ForeignKey, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, declared_attr, mapped_column
from typing import Optional, Type, Generic, Dict, Any, TYPE_CHECKING
from sqlalchemy.sql import select

from fastapi_users.models import UP, ID, OAP

from fastapi_users_db_sqlalchemy.generics import GUID

# class MySQLAlchemyIdeas(Generic[ID]):
#   __tablename__ = "ideas"

#   id: Mapped[UUID_ID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)

UUID_ID = uuid.UUID


class MySQLAlchemyIdea(Generic[ID]):
  if TYPE_CHECKING:  # pragma: no cover
    id: ID
    name: str
    content: str
  else:
    name: Mapped[str] = mapped_column(
      String(length=100), index=True, nullable=False
    )
    content: Mapped[str] = mapped_column(String(length=2000), nullable=False)

class MySQLAlchemyIdeaTableUUID(MySQLAlchemyIdea[UUID_ID]):
  __tablename__ = "idea"
  if TYPE_CHECKING:  # pragma: no cover
    id: UUID_ID
    user_owner_id: UUID_ID
  else:
    id: Mapped[uuid.UUID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)

    @declared_attr
    def user_owner_id(cls) -> Mapped[GUID]:
      return mapped_column(
        GUID, ForeignKey("user.id", ondelete="cascade"), nullable=False
      )


class MySQLAlchemyUserDatabase(SQLAlchemyUserDatabase[UP, ID]):
  def __init__(
      self,
      session: AsyncSession,
      user_table: Type[UP],
      oauth_account_table: Optional[Type[SQLAlchemyBaseOAuthAccountTable]] = None,
  ):
    super().__init__(session, user_table, oauth_account_table)

  # async def get_oauth_access_token(self, oauth: str, user_id: str) -> str | None:
  #   if self.oauth_account_table is None:
  #     raise NotImplementedError()

  #   statement = (
  #     select(self.oauth_account_table.access_token)
  #     .join(self.user_table)
  #     .where(self.oauth_account_table.user_id == user_id)  # type: ignore
  #     .where(self.oauth_account_table.oauth_name == oauth)  # type: ignore
  #   )

  #   results = await self.session.execute(statement)
  #   return results.scalars().first()

  # async def get_by_oauth_account(self, oauth: str, account_id: str) -> Optional[UP]:
  #   print("Testing: get_by_oauth_account Update MySQLAlchemyUserDatabase")
  #   return await super().get_by_oauth_account(oauth, account_id)
  #   if self.oauth_account_table is None:
  #     raise NotImplementedError()

  #   statement = (
  #     select(self.user_table)
  #     .join(self.oauth_account_table)
  #     .where(self.oauth_account_table.oauth_name == oauth)  # type: ignore
  #     .where(self.oauth_account_table.account_id == account_id)  # type: ignore
  #   )
  #   return await self._get_user(statement)

  # async def update_oauth_account(
  #   self, user: UP, oauth_account: OAP, update_dict: Dict[str, Any]
  # ) -> UP:
  #   print("Testing: update_oauth_account Update MySQLAlchemyUserDatabase")
  #   if self.oauth_account_table is None:
  #       raise NotImplementedError()

  #   for key, value in update_dict.items():
  #       setattr(oauth_account, key, value)
  #   self.session.add(oauth_account)
  #   await self.session.commit()

  #   return user
