from fastapi import APIRouter, status
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserInvite
from app.exceptions.user import DuplicateEmailException, UserNotFoundException, InvitationExpiredException
from app.services.datetime import utc_now, ensure_utc
from app.services.auth import hash_password
from app.core.config import settings

router = APIRouter()

@router.post("/invite", status_code=status.HTTP_204_NO_CONTENT)
async def invite_user(data: UserInvite):
	user_with_same_email = await User.find_one(User.email == data.email)
	if user_with_same_email:
		raise DuplicateEmailException(data.email)
	
	user = User(**data.model_dump())
	await user.insert()

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
async def get_users():
	return await User.find_all().to_list()

@router.get("/{email}", response_model=UserResponse)
async def get_user(email: str):
	user = await User.find_one(User.email == email)

	if not user:
		raise UserNotFoundException(email)
	
	return user
