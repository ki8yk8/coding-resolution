from pydantic import BaseModel

class UserLogin(BaseModel):
	email: str
	password: str

class UserVerify(BaseModel):
	email: str
	totp: str

class UserLoginResponse(BaseModel):
	access_token: str
