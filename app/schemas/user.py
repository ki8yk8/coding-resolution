from pydantic import BaseModel, EmailStr, Field
from beanie import PydanticObjectId
from datetime import datetime

class UserInvite(BaseModel):
	email: EmailStr
	name: str = Field(..., min_length=3, max_length=100)

class UserCreate(BaseModel):
	email: EmailStr
	password: str = Field(..., min_length=8)

class UserResponse(BaseModel):
	id: PydanticObjectId
	email: str
	name: str
	created_at: datetime | None
	invited_at: datetime
