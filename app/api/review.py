from app.models.pr_response import PRReviewResponse
import yaml
import os

PROMPT_PATH = os.path.join(os.path.dirname(__file__), '../../config/prompt.yaml')

def load_prompt():
    with open(PROMPT_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def fill_prompt(template: str, variables: dict) -> str:
    return template.format(**variables)

async def generate_review_response(variables: dict, llm_service):
    prompt_yaml = load_prompt()
    prompt = fill_prompt(prompt_yaml['review'], variables)
    review = await llm_service.generate_code_review(prompt)
    return PRReviewResponse(pr_number=variables.get('pr_number', 0), pr_line=1, pr_review_and_suggestion=review) 