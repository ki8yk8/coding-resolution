from fastapi import APIRouter, status
from app.models.user import User
from app.schemas.auth import UserLogin
from app.services.auth import verify_password
from app.exceptions.user import UserNotFoundException
from app.exceptions.auth import CredentialsMismatchException

router = APIRouter()

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(data: UserLogin):
	user_with_email = await User.find_one(User.email == data.email)
	if not user_with_email:
		raise UserNotFoundException(data.email)
	
	if verify_password(data.password, user_with_email.password):
		return
	else:
		raise CredentialsMismatchException()
