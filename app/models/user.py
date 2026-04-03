from beanie import Document
from datetime import datetime, timezone
from pydantic import Field

def utc_now():
	return datetime.now(timezone.utc)

class User(Document):
	email: str
	name: str
	created_at: datetime = Field(default_factory=utc_now)

	class Settings:
		name="users"
