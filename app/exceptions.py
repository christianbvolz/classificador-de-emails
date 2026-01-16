class AppError(Exception):
    """Base exception class for all application-specific errors."""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class LLMServiceError(AppError):
    """Raised when the AI service (OpenAI) fails to process the request."""
    def __init__(self, message: str = "Error processing AI request"):
        super().__init__(message, status_code=502)

class NLPProcessingError(AppError):
    """Raised when the NLP pipeline (spaCy or language detection) fails."""
    def __init__(self, message: str = "Error during text preprocessing"):
        super().__init__(message, status_code=422)