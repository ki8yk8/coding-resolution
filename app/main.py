from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import init_db

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

# first api endpoint
@app.get("/")
def get_hello_world():
	return "Hello World"