from pydantic_settings import BaseSettings
from pydantic import computed_field

class Settings(BaseSettings):
	MONGO_USER: str
	MONGO_PASSWD: str
	MONGO_HOST: str = "localhost"
	MONGO_DB_NAME: str = "mosaic"
	MONGO_PORT: int = 27017

	@computed_field
	@property
	def MONGO_URI(self) -> str:
		return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWD}@{self.MONGO_HOST}:{self.MONGO_DB_NAME}"

	class Config:
		env_file = ".env"

settings = Settings()
