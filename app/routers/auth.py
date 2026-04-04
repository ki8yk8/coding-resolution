from fastapi import APIRouter, status
from app.models.user import User
from app.schemas.auth import UserLogin, AccessToken, UserVerify, TOTP_Setup_Response, UserLoginResponse
from app.services.auth import verify_password, create_access_token, decode_access_token
from app.exceptions.user import UserNotFoundException
from app.exceptions.auth import CredentialsMismatchException, InvalidAccessTokenException, Invalid2FAException
from app.services.totp import generate_qr_URI, verify_totp, create_secret

router = APIRouter()

@router.post("/login", response_model=UserLoginResponse, status_code=status.HTTP_200_OK)
async def login(data: UserLogin):
	user_with_email = await User.find_one(User.email == data.email)
	if not user_with_email:
		raise UserNotFoundException(data.email)
	
	if verify_password(data.password, user_with_email.password):
		return {
			"access_token": create_access_token(user_with_email.model_dump(mode="json"), verified=False)
		}
	else:
		raise CredentialsMismatchException()

@router.get("/{token}", response_model=AccessToken, status_code=status.HTTP_200_OK)
async def about(token: str):
	payload = decode_access_token(token)

	if payload:
		return payload

	raise InvalidAccessTokenException()

@router.post("/setup/{token}", response_model=TOTP_Setup_Response, status_code=status.HTTP_201_CREATED)
async def setup_totp_auth(token: str):
	# validate the user
	payload = decode_access_token(token)

	if not payload:
		raise InvalidAccessTokenException()
	
	# generate hash and send it to the user
	email = payload.get("email")
	user = await User.find_one(User.email == email)

	if not user:
		raise UserNotFoundException(email)
	
	totp_secret = create_secret()
	uri = generate_qr_URI(email, totp_secret)

	user.totp_secret = totp_secret
	await user.save()

	return {
		"uri": uri
	}
	

@router.post("/verify", response_model=UserLoginResponse, status_code=status.HTTP_200_OK)
async def two_factor_authenticate(data: UserVerify):
	# TODO: replace this will middleware looking for token
	user = await User.find_one(User.email == data.email)
	if not User:
		raise UserNotFoundException(data.email)
	
	# validating the totp
	secret = user.totp_secret
	if not verify_totp(secret, data.totp):
		raise Invalid2FAException()

	return {
		"access_token": create_access_token(user.model_dump(mode="json"), verified=True),
	}
