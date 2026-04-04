from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime

class UserLogin(BaseModel):
	email: str
	password: str

class UserVerify(BaseModel):
	email: str
	totp: str

class UserLoginResponse(BaseModel):
	access_token: str

class UserRole(str, Enum):
	ADMIN = "admin"
	USER = "user"
	TEMP_USER = "temp_user"

class AccessToken(BaseModel):
	sub: str
	name: str
	email: EmailStr
	role: UserRole
	iat: datetime
	exp: datetime
