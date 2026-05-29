from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Task Management API is running"}