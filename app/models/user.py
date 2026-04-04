from beanie import Document
from datetime import datetime
from pydantic import Field, EmailStr
from typing import Optional
from app.services.datetime import utc_now

class User(Document):
	email: EmailStr
	name: str
	invited_at: datetime = Field(default_factory=utc_now)
	invited_by: EmailStr
	created_at: Optional[datetime] = None
	totp_secret: Optional[str] = None
	password: Optional[str] = None

	class Settings:
		name="users"
		validate_on_save=True
