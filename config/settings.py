import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
    BACKEND_SUMMARY_ENDPOINT = os.getenv("BACKEND_SUMMARY_ENDPOINT")
    BACKEND_REVIEW_ENDPOINT = os.getenv("BACKEND_REVIEW_ENDPOINT")


settings = Settings()
