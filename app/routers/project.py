from fastapi import APIRouter, status, Depends
from beanie import PydanticObjectId
from app.models.user import User
from app.models.project import Project
from app.schemas.project import ProjectResponse, ProjectCreate, ProjectShareUpdate
from app.dependencies.auth import get_user_details
from app.exceptions.project import ProjectNotFoundException, OnlyAuthorCanDeleteException, OnlyAuthorCanShareException, AlreadySharedException
from app.exceptions.user import UserNotFoundException

router = APIRouter()

@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
async def create_project(data: ProjectCreate, user: User = Depends(get_user_details)):
	project_details = data.model_dump()
	project_details["author_email"] = user.email
	project_details["user_with_access"] = [user.email]

	project = Project(**project_details)
	await project.insert()

	return

@router.get("/", response_model=list[ProjectResponse], status_code=status.HTTP_200_OK)
async def get_all_projects(user: User=Depends(get_user_details)):
	return await Project.find_all().to_list()

@router.get("/{id}", response_model=ProjectResponse, status_code=status.HTTP_200_OK)
async def get_project_by_id(id: PydanticObjectId, user: User=Depends(get_user_details)):
	project = await Project.find_one(Project.id == id)
	if not project:
		raise ProjectNotFoundException(id)
	
	return project

@router.post("/share", status_code=status.HTTP_204_NO_CONTENT)
async def update_project_access(data: ProjectShareUpdate, user: User = Depends(get_user_details)):
	project = await Project.find_one(Project.id == data.id)
	if not project:
		raise ProjectNotFoundException(data.id)
	
	# project sharing by only the author
	if not project.author_email == user.email:
		raise OnlyAuthorCanShareException()
	
	# see if user has already access or not
	if data.email in project.user_with_access or project.author_email == data.email:
		raise AlreadySharedException(data.id, data.email)
	
	# check if the user exists or not
	receipent_user = await User.find_one(User.email == data.email)
	if not receipent_user:
		raise UserNotFoundException(data.email)

	# update the access
	project.user_with_access.append(data.email)
	project.save()

	return

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(id: PydanticObjectId, user: User = Depends(get_user_details)):
	project = await Project.find_one(Project.id == id)
	if not project:
		raise ProjectNotFoundException(id)
	
	# only the author can delete the project
	if not project.author_email == user.email:
		raise OnlyAuthorCanDeleteException()
	
	await project.delete()

	return
