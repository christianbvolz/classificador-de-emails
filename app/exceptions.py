"""Custom exception classes for the email classification API.

Provides structured error handling with HTTP status codes for different
failure scenarios in the processing pipeline.
"""


class AppError(Exception):
    """Base exception for all application-specific errors.

    Attributes:
        message (str): Human-readable error description.
        status_code (int): HTTP status code for the error response.
    """

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class LLMServiceError(AppError):
    """Raised when the LLM service (Groq API) fails to process a request.

    This error indicates temporary service unavailability, rate limiting,
    or other external API failures.

    Attributes:
        status_code (int): Always 502 (Bad Gateway).
    """

    def __init__(self, message: str = "Error processing AI request"):
        super().__init__(message, status_code=502)


class NLPProcessingError(AppError):
    """Raised when the NLP preprocessing pipeline fails.

    This includes failures in spaCy model loading, language detection,
    text cleaning, or lemmatization operations.

    Attributes:
        status_code (int): Always 422 (Unprocessable Entity).
    """

    def __init__(self, message: str = "Error during text preprocessing"):
        super().__init__(message, status_code=422)