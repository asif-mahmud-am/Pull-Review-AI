from anthropic import AsyncAnthropic
from config.settings import settings
from app.services.llm_base import BaseLLMService

class ClaudeService(BaseLLMService):
    """
    Claude LLM service for PR summary and code review generation.
    Implements the BaseLLMService interface for easy swapping.
    """
    def __init__(self):
        self.client = AsyncAnthropic(api_key=settings.CLAUDE_API_KEY)

    async def generate_pr_summary(self, prompt: str) -> str:
        try:
            response = await self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=512,
                temperature=0.5,
                system="You are a code review assistant. Summarize the pull request for a developer audience.",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text if response.content else "No summary generated."
        except Exception as e:
            print(f"Error calling Claude API for summary: {e}")
            return "Could not generate PR summary."

    async def generate_code_review(self, prompt: str) -> str:
        try:
            response = await self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1024,
                temperature=0.7,
                system="You are a code review assistant. Provide actionable, line-by-line feedback on code changes.",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text if response.content else "No review generated."
        except Exception as e:
            print(f"Error calling Claude API for review: {e}")
            return "Could not perform code review."