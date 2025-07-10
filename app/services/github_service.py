import httpx
import hmac
import hashlib
from typing import Dict, Any

class GitHubService:
    def __init__(self, token: str):
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3.diff",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        self.base_url = "https://api.github.com" 

    
    async def get_pr_diff(self, repo_full_name: str, pr_number: int) -> str:
        url = f"{self.base_url}/repos/{repo_full_name}/pulls/{pr_number}.diff"
        print(f"Fetching diff from URL: {url}") 

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text

    async def post_pr_comment(self, repo_full_name: str, pr_number: int, comment_body: str):
        url = f"{self.base_url}/repos/{repo_full_name}/issues/{pr_number}/comments"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json={"body": comment_body})
            response.raise_for_status()
            print(f"Comment posted successfully to {repo_full_name} PR #{pr_number}")

    async def post_inline_comment(self, repo_full_name: str, pr_number: int, commit_id: str, file_path: str, position: int, body: str):
        url = f"{self.base_url}/repos/{repo_full_name}/pulls/{pr_number}/comments"
        payload = {
            "body": body,
            "commit_id": commit_id,
            "path": file_path,
            "position": position
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            print(f"Inline comment posted successfully to {repo_full_name} PR #{pr_number} file {file_path}")

    def verify_webhook_signature(self, payload_body: bytes, secret_token: str, signature_header: str) -> bool:
        if not signature_header:
            return False

        sha_name, signature = signature_header.split('=')
        if sha_name != 'sha256':
            return False

        mac = hmac.new(secret_token.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
        return hmac.compare_digest(mac.hexdigest(), signature)