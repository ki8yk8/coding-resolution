from pydantic import BaseModel, EmailStr, Field, computed_field, field_validator
from datetime import datetime
from typing import Optional

class UserInvite(BaseModel):
	email: EmailStr
	name: str = Field(..., min_length=3, max_length=100)

class UserCreate(BaseModel):
	email: EmailStr
	password: str = Field(..., min_length=8)

class UserResponse(BaseModel):
	id: str
	email: str
	name: str
	created_at: datetime | None
	invited_at: datetime
	
	@field_validator("id", mode="before")
	@classmethod
	def convert_id(cls, v) -> str:
		return str(v)

	# internal field that is read from the model but not exposed as response
	totp_secret: Optional[str] = Field(exclude=True)

	@computed_field(alias="2fa_enabled")
	@property
	def two_fa_enabled(self) -> bool:
		return self.totp_secret is not None
	
	model_config = {
		"from_attributes": True,
		"serialize_by_alias": True,
	}

