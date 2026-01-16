import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from .schemas import EmailRequest, EmailResponse
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

@app.post("/process-email", response_model=EmailResponse)
async def process_email(request: EmailRequest):
    return classify_and_respond(request.content)