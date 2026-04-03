from beanie import Document
from datetime import datetime, timezone
from pydantic import Field, EmailStr
from typing import Annotated

def utc_now():
	return datetime.now(timezone.utc)

class User(Document):
	email: EmailStr
	name: str
	created_at: datetime = Field(default_factory=utc_now)

	class Settings:
		name="users"
		validate_on_save=True
