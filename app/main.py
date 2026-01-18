"""FastAPI application for email classification and automated response generation.

This module defines the main API endpoint that accepts batches of emails,
processes them through an LLM-powered classification pipeline, and returns
suggested responses for each email.
"""

import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from .schemas import EmailListRequest, EmailResponse
from .services import classify_and_respond
from .exceptions import AppError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Email Classifier",
    description="High-performance email analysis using Llama 3 on Groq LPUs.",
    version="1.1.0"
)

@app.exception_handler(AppError)
async def app_exception_handler(request: Request, exc: AppError):
    logger.warning(f"Handled exception: {exc.message} ({exc.__class__.__name__})")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "code": exc.__class__.__name__}
    )

@app.post("/process-email", response_model=List[EmailResponse])
async def process_email(request: EmailListRequest):
    """Process a batch of emails and generate suggested responses.

    Analyzes each email using an LLM-powered pipeline to classify productivity
    and generate contextually appropriate response suggestions.

    Args:
        request (EmailListRequest): Batch request containing 1-10 emails,
            each with `subject` and `body` fields.

    Returns:
        List[EmailResponse]: A list of response objects for each input email,
            containing classification results (`isProductive`), suggested
            subject/body, detected language, and the original email text.

    Raises:
        HTTPException:
            - 422: Invalid request format or constraint violation (empty list,
              >10 emails, or missing required fields).
            - 502: LLM service failure (see `LLMServiceError`).

    Example Request:
        ```json
        {
            "emails": [
                {"subject": "Overdue Invoice", "body": "I cannot pay my invoice."},
                {"subject": "Happy Holidays", "body": "Merry Christmas!"}
            ]
        }
        ```

    Notes:
        - Each email triggers an independent LLM API call; provider rate
          limits may apply.
        - Maximum batch size: 10 emails per request.
        - Responses are generated in the same language as the input.
    """
    
    # Process each email sequentially
    results = []
    for email_item in request.emails:
        # Combine subject and body for processing
        full_email_text = f"Subject: {email_item.subject}\n\nBody: {email_item.body}"
        
        result = classify_and_respond(full_email_text)
        results.append(result)
    
    return results