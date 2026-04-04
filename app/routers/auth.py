from fastapi import APIRouter, status, Response, Depends
from app.models.user import User
from app.schemas.auth import UserLogin, AccessToken, UserVerify, TOTP_Setup_Response 
from app.services.auth import verify_password, create_access_token, decode_access_token
from app.exceptions.user import UserNotFoundException
from app.exceptions.auth import CredentialsMismatchException, Invalid2FAException
from app.services.totp import generate_qr_URI, verify_totp, create_secret
from app.core.config import settings
from app.dependencies.auth import get_access_token_payload, get_user_details

router = APIRouter()

@router.post("/login", status_code=status.HTTP_204_NO_CONTENT)
async def login(data: UserLogin, response: Response):
	user_with_email = await User.find_one(User.email == data.email)
	if not user_with_email:
		raise UserNotFoundException(data.email)
	
	if not verify_password(data.password, user_with_email.password):
		raise CredentialsMismatchException()

	access_token = create_access_token(user_with_email.model_dump(mode="json"), verified=False)
	response.set_cookie(
		key="access_token",
		value=access_token,
		httponly=True,
		secure=True,
		samesite="lax",
		max_age=int(settings.AUTH_EXPIRY.total_seconds()),
	)

	return

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response, payload: AccessToken = Depends(get_access_token_payload)):
	response.delete_cookie(
		key="access_token",
		httponly=True,
		secure=True,
		samesite="lax",
	)

	return 

@router.get("/", response_model=AccessToken, status_code=status.HTTP_200_OK)
async def about(payload:AccessToken = Depends(get_access_token_payload)):
	return payload

@router.post("/2fa/setup", response_model=TOTP_Setup_Response, status_code=status.HTTP_201_CREATED)
async def setup_totp_auth(user: User = Depends(get_user_details)):
	totp_secret = create_secret()
	uri = generate_qr_URI(user.email, totp_secret)

	user.totp_secret = totp_secret
	await user.save()

	return {
		"uri": uri
	}
	
@router.post("/verify", status_code=status.HTTP_204_NO_CONTENT)
async def two_factor_authenticate(response: Response, data: UserVerify, user: User = Depends(get_user_details)):
	# validating the totp
	secret = user.totp_secret
	if not verify_totp(secret, data.totp):
		raise Invalid2FAException()

	access_token = create_access_token(user.model_dump(mode="json"), verified=True)
	response.set_cookie(
		key="access_token",
		value=access_token,
		httponly=True,
		secure=True,
		samesite="lax",
		max_age=int(settings.AUTH_EXPIRY.total_seconds()),
	)

	return
