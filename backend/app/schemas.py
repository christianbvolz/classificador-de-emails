from pydantic import BaseModel, Field, ConfigDict, conlist
from pydantic.alias_generators import to_camel
from typing import Optional, List

class Email(BaseModel):
    """Represents an email with subject and body.

    Used as an item within batch requests.
    """
    subject: str = Field(..., description="Email subject line.")
    body: str = Field(..., description="Email body content.")

class EmailListRequest(BaseModel):
    """Request model for batch processing of emails.

    Enforces 1–10 items in the `emails` list.
    """
    emails: conlist(Email, min_length=1, max_length=10) = Field(
        ...,
        description="List of 1-10 emails to process"
    )

class EmailResponse(BaseModel):
    """Analysis result for a single email.

    Contains classification flags, suggested subject/body, detected language,
    category, and the original email text.
    """
    is_productive: bool
    category: Optional[str] = None
    suggested_subject: str
    suggested_body: str
    detected_language: Optional[str] = None
    original_email: Email

    # Pydantic configuration for naming conventions and documentation
    model_config = ConfigDict(
        alias_generator=to_camel,  # is_productive -> isProductive
        populate_by_name=True,     # Allows internal Python usage of original names
        json_schema_extra={
            "example": {
                "isProductive": True,
                "category": "technical_support",
                "suggestedSubject": "Re: Technical Support Request",
                "suggestedBody": "Dear customer, we received your request...",
                "detectedLanguage": "en",
                "originalEmail": {
                    "subject": "Help with system",
                    "body": "I need assistance with the login process."
                }
            }
        }
    )