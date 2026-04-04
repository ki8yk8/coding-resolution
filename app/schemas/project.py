from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime

class ProjectCreate(BaseModel):
	name: str

class ProjectShareUpdate(BaseModel):
	id: str
	email: EmailStr

class ProjectResponse(BaseModel):
	id: str
	name: str
	author_email: EmailStr
	category: str
	created_at: datetime
	last_updated_on: datetime

	@field_validator("id", mode="before")
	@classmethod
	def convert_id(cls, v) -> str:
		return str(v)
	
	model_config = {
		"from_attributes": True,
	}