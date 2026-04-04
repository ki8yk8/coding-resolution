from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import init_db
from app.routers import user, auth, project

@asynccontextmanager
async def lifespan(app: FastAPI):
	try:
		# establish connection with mongodb on startup
		await init_db()
		print("SUCCESS: Database connection established correctly")
	except Exception as e:
		print(f"ERROR: {e}")
	
	yield

app = FastAPI(debug=True, lifespan=lifespan)

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(project.router, prefix="/projects", tags=["projects"])

# status route that can be used to test the backend
@app.get("/")
def get_status():
	return "okay"