from beanie import Document
from datetime import datetime

class User(Document):
	email: str
	name: str
	created_at: datetime

	class Settings:
		name="users"
