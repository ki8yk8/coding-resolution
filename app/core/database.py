from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie    # ODM wrapper
from app.core.config import settings
from app.models.user import User
from app.models.project import Project

async def init_db():
	# establishes the raw connection with mongodb while making it non-blockable for fastapi
	client = AsyncIOMotorClient(settings.MONGO_URI)

	await init_beanie(
		database=client[settings.MONGO_DB_NAME],
		document_models=[User, Project],
	)
