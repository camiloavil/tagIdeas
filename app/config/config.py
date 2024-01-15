from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  model_config = SettingsConfigDict(env_file="test.env")
  port : int = 8000
  app_name: str = "Test TagIdeas"
  app_secret: str = "SECRET"
  app_lifetime: int = 3600
  app_google_client_id: str = ""
  app_google_client_secret: str = ""
  # db_name: str = "testUsers"
  # db_user: str = "test"
  # db_password: str = "test"
  # db_host: str = "localhost:27017"
  # db_srv: bool = False

  # @property
  # def db_url(self) -> MongoDsn:
  #     return f"mongodb{'+srv' if self.db_srv else ''}://{self.db_user}:{self.db_password}@{self.db_host}"


# settings = Settings()
#this is if config loads from the beginning
@lru_cache
def get_settings() -> Settings:
  return Settings()