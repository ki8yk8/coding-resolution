from pydantic import BaseModel

class ProjectCreate(BaseModel):
	name: str

class ProjectResponse(BaseModel):
	name: str
	authorEmail: str
	category: str
	created_at: str
	last_updated_on: str
