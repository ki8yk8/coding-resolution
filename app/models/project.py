from beanie import Document
from datetime import datetime
from app.services.datetime import utc_now
from pydantic import Field, EmailStr
from typing import List

class Project(Document):
	name: str
	authorEmail: EmailStr
	category: str = "Neo-GutHalu"
	created_at: datetime = Field(default_factory=utc_now)
	last_updated_on: datetime = Field(default_factory=utc_now)
	user_with_access: List[EmailStr] = []

	class Settings:
		name="projects"
		validate_on_save=True
