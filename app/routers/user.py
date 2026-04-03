from fastapi import APIRouter, HTTPException
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from beanie import PydanticObjectId

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(data: UserCreate):
	user = User(**data.model_dump())
	await user.insert()

	return user

@router.get("/", response_model=list[UserResponse])
async def get_users():
	return await User.find_all().to_list()

@router.get("/{email}", response_model=UserResponse)
async def get_user(email: str):
	user = await User.find(User.email == email)

	if not user:
		raise HTTPException(status_code=404, detail="User not found")
	
	return user
