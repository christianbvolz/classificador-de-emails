from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Optional

class EmailRequest(BaseModel):
    """Schema for incoming email analysis requests."""
    content: str = Field(..., description="Raw text of the email.")

class EmailResponse(BaseModel):
    """
    Schema for the analysis result.
    Uses an alias generator to automatically convert snake_case to camelCase.
    """
    is_productive: bool
    suggested_subject: str
    suggested_body: str
    detected_language: Optional[str] = None

    # Pydantic configuration for naming conventions and documentation
    model_config = ConfigDict(
        alias_generator=to_camel,  # is_productive -> isProductive
        populate_by_name=True,     # Allows internal Python usage of original names
        json_schema_extra={
            "example": {
                "isProductive": True,
                "suggestedSubject": "Re: Technical Support Request",
                "suggestedBody": "Dear customer, we received your request...",
                "detectedLanguage": "en"
            }
        }
    )