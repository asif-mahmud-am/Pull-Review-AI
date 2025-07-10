import google.generativeai as genai
from config.settings import settings

class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)

    async def gemini_flash_summary_agent(self, text: str) -> str:
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = await model.generate_content_async(
                f"Summarize the following code changes and generate concise release notes:\n\n{text}"
            )
            return response.text
        except Exception as e:
            print(f"Error calling Gemini Flash API: {e}")
            return "Could not generate summary."

    async def gemini_pro_review_agent(self, code_diff: str, context: str = "") -> str:
        try:
            model = genai.GenerativeModel('gemini-1.5-pro')
            prompt = f"Review the following code diff for potential bugs, style violations, and suggest improvements. {context}\n\nCode Diff:\n{code_diff}"
            response = await model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            print(f"Error calling Gemini Pro API: {e}")
            return "Could not perform Gemini Pro review."