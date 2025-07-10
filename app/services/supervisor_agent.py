from app.services.github_service import GitHubService
from app.services.groq_service import GroqService
from app.services.gemini_service import GeminiService
from app.models.pr_event import PullRequestEvent
import re

class SupervisorAgent:
    def __init__(self, github_token: str):
        self.github_service = GitHubService(github_token)
        self.groq_service = GroqService()
        self.gemini_service = GeminiService()

    async def handle_pull_request_event(self, event: PullRequestEvent):
        pr_number = event.get_pull_request_number()
        repo_full_name = event.get_repo_full_name()
        # diff_url = event.get_diff_url()
        pr_title = event.get_pull_request_title()

        print(f"Received PR event for {repo_full_name} PR #{pr_number}")

        if event.action == "opened" or event.action == "synchronize":
            # 1. Get the diff
            diff_content = await self.github_service.get_pr_diff(repo_full_name, pr_number)
            if not diff_content:
                print(f"No diff content found for PR #{pr_number}")
                return

            # 2. PR Summarization (using Gemini 1.5 Flash)
            summary_prompt = f"Pull Request Title: {pr_title}\n\nCode Changes:\n{diff_content}\n\nSummarize these changes concisely and provide brief release notes."
            summary = await self.gemini_service.gemini_flash_summary_agent(summary_prompt)
            await self.github_service.post_pr_comment(repo_full_name, pr_number, f"**AI PR Summary:**\n\n{summary}")
            print(f"Posted summary for PR #{pr_number}")

            # 3. Basic Line-by-Line Code Review (using Groq's Llama and/or Gemini 1.5 Pro)
            llama_review_prompt = f"Perform a basic line-by-line code review of the following diff. Point out obvious bugs, style issues, and suggest minor improvements.\n\nCode Diff:\n{diff_content}"
            llama_review_feedback = await self.groq_service.llama_review_agent(llama_review_prompt)
            await self.github_service.post_pr_comment(repo_full_name, pr_number, f"**AI Code Review (Llama via Groq):**\n\n{llama_review_feedback}")
            print(f"Posted Llama review for PR #{pr_number}")

            gemini_pro_review_feedback = await self.gemini_service.gemini_pro_review_agent(diff_content, "Focus on basic bug detection and adherence to general coding practices.")
            await self.github_service.post_pr_comment(repo_full_name, pr_number, f"**AI Code Review (Gemini Pro):**\n\n{gemini_pro_review_feedback}")
            print(f"Posted Gemini Pro review for PR #{pr_number}")


        else:
            print(f"Unhandled PR action: {event.action}")

  
    def extract_commit_id(self, diff_content: str) -> str:
        match = re.search(r'From ([0-9a-fA-F]{40})', diff_content)
        if match:
            return match.group(1)
        return "HEAD" # Fallback