from fastapi import APIRouter, Request, BackgroundTasks
from app.models.pr_event import PRPayloadV2, PRFileInfo
from app.api.summary import generate_summary_response
from app.api.review import generate_review_response
from app.services.claude_service import ClaudeService
import httpx
import os

supervisor = APIRouter(prefix="/ai_agent", tags=["Supervisor"])

# These should be set to the backend endpoints for posting summary and review results
BACKEND_SUMMARY_ENDPOINT = os.getenv("BACKEND_SUMMARY_ENDPOINT", "http://backend/summary")
BACKEND_REVIEW_ENDPOINT = os.getenv("BACKEND_REVIEW_ENDPOINT", "http://backend/review")

@supervisor.post("/")
async def supervisor_pr_review(payload: PRPayloadV2, background_tasks: BackgroundTasks):
    llm_service = ClaudeService()
    pr = payload.pull_request
    pr_number = pr["pr_number"]
    pr_title = pr["pr_title"]
    pr_description = pr.get("pr_body", "")
    author_name = pr.get("pr_user", "")
    repo_structure_summary = pr.get("pr_repo_name", "")
    changed_files = list(pr["pr_files"].keys())
    pr_diff = "\n\n".join([
        file_info[f"{file_key}_diff"]
        for file_key, file_info in pr["pr_files"].items()
    ])

    summary_variables = {
        "pr_title": pr_title,
        "pr_description": pr_description,
        "author_name": author_name,
        "changed_files": ", ".join(changed_files),
        "repo_structure_summary": repo_structure_summary,
        "pr_diff": pr_diff
    }
    summary = await generate_summary_response(summary_variables, llm_service)
    async with httpx.AsyncClient() as client:
        await client.post(BACKEND_SUMMARY_ENDPOINT, json=summary.dict())
        for file_key, file_info in pr["pr_files"].items():
            review_variables = {
                "pr_title": pr_title,
                "pr_description": pr_description,
                "author_name": author_name,
                "changed_files": file_info[f"{file_key}_name"],
                "repo_structure_summary": repo_structure_summary,
                "pr_diff": file_info[f"{file_key}_diff"]
            }
            review = await generate_review_response(review_variables, llm_service)
            await client.post(BACKEND_REVIEW_ENDPOINT, json=review.dict())
    return {"status": "completed"} 