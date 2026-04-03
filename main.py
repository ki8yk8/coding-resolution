from fastapi import FastAPI

app = FastAPI(debug=True)

# first api endpoint
@app.get("/")
def get_hello_world():
	return "Hello World"