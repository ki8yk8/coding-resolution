from fastapi import APIRouter, HTTPException
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(data: UserCreate):
	user_with_same_email = User.find(User.email == data.email)
	if user_with_same_email:
		raise HTTPException(status_code=400, detail="Multiple users with same email cannot be created")

	user = User(**data.model_dump())
	await user.insert()

	return user

@router.get("/", response_model=list[UserResponse])
async def get_users():
	return await User.find_all().to_list()

@router.get("/{email}", response_model=UserResponse)
async def get_user(email: str):
	user = await User.find_one(User.email == email)

	if not user:
		raise HTTPException(status_code=404, detail="User not found")
	
	return user
