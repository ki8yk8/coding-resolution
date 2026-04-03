from pydantic import BaseModel
from beanie import PydanticObjectId
from datetime import datetime

class UserCreate(BaseModel):
	email: str
	name: str

class UserResponse(BaseModel):
	id: PydanticObjectId
	email: str
	name: str
	created_at: datetime
