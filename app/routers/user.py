from fastapi import APIRouter, status, Depends
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserInvite
from app.exceptions.user import DuplicateEmailException, UserNotFoundException, InvitationExpiredException
from app.services.datetime import utc_now, ensure_utc
from app.services.auth import hash_password
from app.core.config import settings
from app.dependencies.auth import get_user_details

router = APIRouter()

@router.post("/invite", status_code=status.HTTP_204_NO_CONTENT)
async def invite_user(data: UserInvite, user: User = Depends(get_user_details)):
	user_with_same_email = await User.find_one(User.email == data.email)
	if user_with_same_email:
		raise DuplicateEmailException(data.email)
	
	new_user_details = data.model_dump()
	new_user_details["invited_by"] = user.email
	new_user = User(**new_user_details)
	await new_user.insert()

	return

# TODO: refactor with transfer of business logic to the services
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate):
	# check if the invitation for user exists or not
	user_with_invite = await User.find_one(User.email == data.email)
	if not user_with_invite:
		raise UserNotFoundException(data.email)
	
	# check if user has already accepted the invite
	if user_with_invite.created_at:
		raise DuplicateEmailException(data.email)

	# check if invite has expired or not
	time_diff = utc_now() - ensure_utc(user_with_invite.invited_at)
	if time_diff > settings.INVITE_EXPIRY:
		raise InvitationExpiredException(data.email)

	user_with_invite.password = hash_password(data.password)
	user_with_invite.created_at = utc_now()
	await user_with_invite.save()

	return

@router.get("/", response_model=list[UserResponse])
async def get_users(user: User = Depends(get_user_details)):
	return await User.find_all().to_list()

@router.get("/{email}", response_model=UserResponse)
async def get_user(email: str, user: User = Depends(get_user_details)):
	user = await User.find_one(User.email == email)

	if not user:
		raise UserNotFoundException(email)
	
	return user
