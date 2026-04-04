from fastapi import Request
from app.models.user import User
from app.schemas.auth import AccessToken
from app.services.auth import decode_access_token
from app.exceptions.auth import ForbiddenAccessException, InvalidAccessTokenException
from app.exceptions.user import UserNotFoundException

async def get_user_details(request: Request)->User:
	token = request.cookies.get("access_token")

	if not token:
		raise ForbiddenAccessException()

	payload = decode_access_token(token)
	if not payload:
		raise InvalidAccessTokenException()
	
	email = payload["email"]
	user_with_email = await User.find_one(User.email == email)
	if not user_with_email:
		raise UserNotFoundException()
	
	return user_with_email

async def get_access_token_payload(request: Request)->AccessToken:
	token = request.cookies.get("access_token")

	if not token:
		raise ForbiddenAccessException()
	
	payload = decode_access_token(token)
	if not payload:
		raise InvalidAccessTokenException()
	
	return payload
	