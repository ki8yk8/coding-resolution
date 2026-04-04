from fastapi import APIRouter, status
from app.models.user import User
from app.schemas.auth import UserLogin, AccessToken
from app.services.auth import verify_password, create_access_token, decode_access_token
from app.exceptions.user import UserNotFoundException
from app.exceptions.auth import CredentialsMismatchException, InvalidAccessTokenException

router = APIRouter()

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(data: UserLogin):
	user_with_email = await User.find_one(User.email == data.email)
	if not user_with_email:
		raise UserNotFoundException(data.email)
	
	if verify_password(data.password, user_with_email.password):
		return create_access_token(user_with_email.model_dump(mode="json"), verified=False)
	else:
		raise CredentialsMismatchException()

@router.get("/{token}", response_model=AccessToken, status_code=status.HTTP_200_OK)
async def about(token: str):
	payload = decode_access_token(token)

	if payload:
		return payload

	raise InvalidAccessTokenException()
