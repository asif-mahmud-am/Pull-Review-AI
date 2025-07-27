from fastapi import FastAPI
from app.api.supervisor import supervisor

app = FastAPI(title="AI-Powered PR Reviewer")

app.include_router(supervisor)

@app.get("/")
async def root():
    return {"message": "AI-Powered PR Reviewer is running!"}