from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
	email: str
	name: str

class UserResponse(BaseModel):
	id: str
	email: str
	name: str
	created_at: datetime
