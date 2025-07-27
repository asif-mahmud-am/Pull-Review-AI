# pull-reviewer-ai

## API Endpoints

### PR Summary
- **POST** `/pr/summary`
- **Request Body:** PR webhook payload (see `app/models/pr_event.py`)
- **Response:**
```
{
  "pr_number": 1,
  "pr_line": 1,
  "pr_summary": "..."
}
```

### PR Review
- **POST** `/pr/review`
- **Request Body:** PR webhook payload (see `app/models/pr_event.py`)
- **Response:**
```
{
  "pr_number": 1,
  "pr_line": 1,
  "pr_review_and_suggestion": "..."
}
```

## LLM Service
- Uses Groq Llama by default. To swap LLM, implement `BaseLLMService` and update the dependency in `app/api/pr.py`.

## Development
- Endpoints use dummy payloads for now. Integrate with real webhook events as needed.