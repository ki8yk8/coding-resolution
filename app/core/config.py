from pydantic_settings import BaseSettings
from pydantic import computed_field
from datetime import timedelta

class Settings(BaseSettings):
	MONGO_USER: str = "admin"
	MONGO_PASSWD: str = "password"
	MONGO_HOST: str = "localhost"
	MONGO_DB_NAME: str = "mosaic"
	MONGO_PORT: int = 27017
	AUTH_SECRET: str
	AUTH_EXPIRY: timedelta = timedelta(days=1)
	INVITE_EXPIRY: timedelta = timedelta(weeks=1)
	MONGO_URL: str | None = None

	@computed_field
	@property
	def MONGO_URI(self) -> str:
		if self.MONGO_URL:
			return self.MONGO_URL
		
		return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWD}@{self.MONGO_HOST}:{self.MONGO_PORT}"

	class Config:
		env_file = ".env"

settings = Settings()
