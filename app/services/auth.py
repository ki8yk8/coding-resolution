from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import jwt
from app.schemas.user import UserResponse
from app.services.datetime import utc_now
from app.core.config import settings

ph = PasswordHasher()

def hash_password(password: str) -> str:
	return ph.hash(password)

def verify_password(password:str, hash: str) -> bool:
	try:
		return ph.verify(hash, password)
	except VerifyMismatchError:
		return False

def create_access_token(user:dict, verified:bool=False)->str:
	user = UserResponse(**user)

	now = utc_now()
	payload = {
		"sub": user.id,
		"name": user.name,
		"email": user.email,
		"role": "user" if verified else "temp_user",
		"iat": now,
		"exp": now+settings.AUTH_EXPIRY
	}
	token = jwt.encode(payload, settings.AUTH_SECRET, algorithm="HS256")
	return token

def decode_access_token(token:str):
	try:
		payload = jwt.decode(token, settings.AUTH_SECRET, algorithms=["HS256"])
		
		return payload
	except jwt.ExpiredSignatureError:
		return None
	except jwt.InvalidTokenError:
		return None
