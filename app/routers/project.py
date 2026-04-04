from fastapi import APIRouter, status
from typing import List
from app.schemas.project import ProjectResponse
from app.schemas.project import ProjectCreate

router = APIRouter()

@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
def create_project(data: ProjectCreate):
	pass

@router.get("/", response_model=List[ProjectResponse], status_code=status.HTTP_200_OK)
def get_all_projects():
	pass

@router.get("/{id}", response_model=ProjectResponse, status_code=status.HTTP_200_OK)
def get_project_by_id(id: str):
	pass

@router.put("/share/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_project_access(id: str):
	pass
