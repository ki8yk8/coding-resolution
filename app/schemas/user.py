from pydantic import BaseModel, EmailStr, Field
from beanie import PydanticObjectId
from datetime import datetime
from typing import Annotated

class UserCreate(BaseModel):
	email: EmailStr
	name: Annotated[str, Field(None, min_length=3, max_length=100)]

class UserResponse(BaseModel):
	id: PydanticObjectId
	email: str
	name: str
	created_at: datetime
