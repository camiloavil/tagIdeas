import uuid
from typing import Optional

from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
  AuthenticationBackend,
  BearerTransport,
  JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase

from app.db import User, get_user_db
from app.config import get_settings
from .MyGoogleOAuth2 import MyGoogleOAuth2

SECRET = get_settings().app_secret

google_oauth_client = MyGoogleOAuth2(
  client_id=get_settings().app_google_client_id,
  client_secret=get_settings().app_google_client_secret,
)
#Original piece of code: It works
# google_oauth_client = GoogleOAuth2(
#   client_id=get_settings().app_google_client_id,
#   client_secret=get_settings().app_google_client_secret,
#)

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
  reset_password_token_secret = SECRET
  verification_token_secret = SECRET

  async def on_after_login(self, user: User, request: Request = None,
    response: Response = None
  ) -> None:
    print(f"User {user.email} logged in.")

  async def on_after_register(self, user: User, request: Request = None,
    response: Response = None
  ) -> None:
    if google_oauth_client is not None:
      user_access_token: str = next((oauth_account.access_token for oauth_account in user.oauth_accounts
                                    if oauth_account.oauth_name == google_oauth_client.name), None)
      if user_access_token:
        oauth_user_info = await google_oauth_client.get_OAuth_info(user_access_token)
        await self.user_db.update(user, oauth_user_info)

  async def on_after_forgot_password(
    self, user: User, token: str, request: Optional[Request] = None
  ):
    print(f"User {user.id} has forgot their password. Reset token: {token}")

  async def on_after_request_verify(
    self, user: User, token: str, request: Optional[Request] = None
  ):
    print(f"Verification requested for user {user.id}. Verification token: {token}")

async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
  yield UserManager(user_db)

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
  return JWTStrategy(secret=SECRET, lifetime_seconds=get_settings().app_lifetime)

auth_backend = AuthenticationBackend(
  name="jwt",
  transport=bearer_transport,
  get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
