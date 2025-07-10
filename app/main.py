from fastapi import FastAPI, Request, HTTPException, Header
from app.models.pr_event import PullRequestEvent
from app.services.supervisor_agent import SupervisorAgent
from app.services.github_service import GitHubService
from config.settings import settings
import json
from pydantic import ValidationError 

app = FastAPI(title="AI-Powered PR Reviewer")


github_service = GitHubService(settings.GITHUB_ACCESS_TOKEN)  
supervisor_agent = SupervisorAgent(settings.GITHUB_ACCESS_TOKEN)

@app.post("/webhook")
async def github_webhook(request: Request, x_hub_signature_256: str = Header(None)):
    payload_body = await request.body()

    if not github_service.verify_webhook_signature(payload_body, settings.GITHUB_WEBHOOK_SECRET, x_hub_signature_256):
        raise HTTPException(status_code=403, detail="Invalid signature")

    try:
        payload_json = json.loads(payload_body)
        event = PullRequestEvent(**payload_json) 
    except ValidationError as e: 
        print(f"Pydantic validation error: {e.errors()}")
        raise HTTPException(status_code=400, detail=f"Invalid payload structure: {e.errors()}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f"Payload body received: {payload_body.decode()}")
        raise HTTPException(status_code=400, detail=f"Invalid JSON payload: {e}")
    except Exception as e:
        print(f"General payload processing error: {e}")
        raise HTTPException(status_code=400, detail=f"General payload error: {e}")

    if event.action in ["opened", "synchronize", "reopened"]:
        await supervisor_agent.handle_pull_request_event(event)
    else:
        print(f"Skipping action: {event.action}")

    return {"message": "Event received and processed."}

@app.get("/")
async def root():
    return {"message": "AI-Powered PR Reviewer is running!"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8800, log_level="info",reload=False)