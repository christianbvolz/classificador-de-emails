"""Business logic for email classification and response generation.

This module orchestrates the NLP preprocessing pipeline and LLM interaction
to analyze emails and generate suggested responses using the Groq API.
"""

import os
import json
import logging
from groq import Groq
from dotenv import load_dotenv
from .utils import clean_email_text
from .exceptions import LLMServiceError
from .templates import RESPONSE_TEMPLATES, CATEGORY_DESCRIPTIONS, get_all_categories

load_dotenv()

# Initialize the Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
logger = logging.getLogger(__name__)

def classify_and_respond(email_content: str) -> dict:
    """Classify an email and generate a suggested response.

    Orchestrates the complete processing pipeline: NLP cleaning, language
    detection, LLM classification via Groq API, response generation, and
    validation with fallback to templates when needed.

    Token Optimization Strategy:
        - Sends only few-shot examples for detected language (not both PT/EN)
        - Uses simplified category descriptions (6 categories listed inline)
        - Includes only 3 representative examples instead of all 12
        - Condensed instructions reduce input tokens by ~60%
        - Expected token usage: ~400-700 tokens/request (input + output)

    Args:
        email_content (str): Raw email text (typically formatted as
            "Subject: ...\n\nBody: ...").

    Returns:
        dict: Classification and response metadata with keys:
            - is_productive (bool): True if email requires action.
            - category (str): One of 6 categories (payment_issue, technical_support, etc.)
            - suggested_subject (str): Professional subject line for reply.
            - suggested_body (str): Complete response email body.
            - detected_language (str): ISO language code (e.g., 'pt', 'en').
            - original_email (str): Original input email for reference.

    Raises:
        LLMServiceError: If the Groq API service is unavailable or fails
            after retries.

    Notes:
        - Falls back to predefined templates if LLM response validation fails.
        - Logs classification metrics (productivity, category, language, token usage).
    """
    original_email = email_content
        
    # Step 1: Pre-process text using our NLP pipeline
    cleaned_text, lang = clean_email_text(email_content)

    # Step 2: Optimized prompt with minimal examples (only detected language)
    # Simplified category list
    categories_info = (
        "CATEGORIES:\n"
        "payment_issue | technical_support | information_request | "
        "greeting | complaint | spam"
    )
    
    # Build few-shot examples ONLY for detected language (reduces tokens by ~50%)
    examples_text = "\nEXAMPLES:\n"
    if lang in RESPONSE_TEMPLATES:
        # Select 3 representative categories only
        key_categories = ["payment_issue", "technical_support", "greeting"]
        for category_name in key_categories:
            if category_name in RESPONSE_TEMPLATES[lang]:
                template = RESPONSE_TEMPLATES[lang][category_name]
                is_prod = category_name not in ["greeting", "spam"]
                examples_text += f"{category_name}: {{\"is_productive\": {str(is_prod).lower()}, "
                examples_text += f"\"category\": \"{category_name}\", "
                examples_text += f"\"suggested_subject\": \"{template['subject']}\"}}\n"
    
    system_prompt = (
    "You are a Customer Support AI. Analyze emails and draft professional responses.\n\n"
    
    f"{categories_info}\n\n"
    
    "INSTRUCTIONS:\n"
    "1. Identify category from list above\n"
    "2. Use CLEANED text for analysis, ORIGINAL for personalization (names, numbers)\n"
    "3. Response as appropriate team (Financial/Technical/Customer Service)\n"
    "4. Tone: Professional and empathetic (adjust by category)\n"
    "5. Structure: 3 paragraphs, 100-250 words\n"
    "6. is_productive=true for: payment_issue, technical_support, information_request, complaint\n\n"
    
    f"{examples_text}\n"
    "Return JSON: is_productive (bool), category (string), suggested_subject, suggested_body."
)

    try:
        # Step 3: Call Groq Cloud API with optimized parameters
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Original email:\n{email_content}\n\nCleaned text for analysis:\n{cleaned_text}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.3,  # Balance between creativity and consistency
            max_tokens=600    # Optimized limit (reduced from 800)
        )

        ai_data = json.loads(completion.choices[0].message.content)

        # Validate response quality; if invalid, use fallback template
        if not _validate_response(ai_data):
            logger.warning("Validation failed. Using fallback template.")
            category = ai_data.get("category", "technical_support" if ai_data.get("is_productive", True) else "greeting")
            ai_data = _get_fallback_response(lang, category)

        # Add metadata
        ai_data["detected_language"] = lang
        ai_data["original_email"] = original_email

        # Log for monitoring and improvements
        logger.info(
            f"Classification complete - Productive: {ai_data.get('is_productive')}, "
            f"Category: {ai_data.get('category', 'N/A')}, "
            f"Lang: {lang}, "
            f"Tokens: {completion.usage.total_tokens if hasattr(completion, 'usage') else 'N/A'}"
        )

        return ai_data

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        fallback = _get_fallback_response(lang, "technical_support")
        fallback["original_email"] = original_email
        return fallback

    except Exception as e:
        logger.error(f"Groq service failure: {e}")
        raise LLMServiceError("The AI service is currently unavailable via Groq.")


def _validate_response(ai_data: dict) -> bool:
    """Validate LLM response quality and completeness.

    Checks that all required fields are present and meet minimum content
    length requirements for subject and body.

    Args:
        ai_data (dict): Parsed JSON response from the LLM.

    Returns:
        bool: True if response meets quality standards, False otherwise.
    """
    # Check required fields
    required_fields = ["is_productive", "category", "suggested_subject", "suggested_body"]
    if not all(field in ai_data for field in required_fields):
        return False
    
    # Check minimum content length
    if len(ai_data.get("suggested_body", "")) < 50:
        return False
    
    if len(ai_data.get("suggested_subject", "")) < 5:
        return False
    
    # Validate category
    if ai_data.get("category") not in get_all_categories():
        return False
    
    return True


def _get_fallback_response(lang: str, category: str) -> dict:
    """Generate a template-based fallback response.

    Used when LLM response generation fails or validation does not pass.
    Selects an appropriate predefined template based on language and category.

    Args:
        lang (str): Detected language code (e.g., 'pt', 'en').
        category (str): Email category (payment_issue, technical_support, etc.).

    Returns:
        dict: Fallback response with keys: `is_productive`, `category`, 
            `suggested_subject`, `suggested_body`, `detected_language`.

    Notes:
        - Defaults to Portuguese templates if language is not supported.
        - Defaults to 'technical_support' category if specified category not found.
    """
    # Default to Portuguese if language not in templates
    template_lang = lang if lang in RESPONSE_TEMPLATES else "pt"
    
    # Default to technical_support if category not found
    if category not in RESPONSE_TEMPLATES[template_lang]:
        category = "technical_support"
    
    template = RESPONSE_TEMPLATES[template_lang][category]
    
    # Determine if category is productive
    is_productive = category not in ["greeting", "spam"]
    
    return {
        "is_productive": is_productive,
        "category": category,
        "suggested_subject": template["subject"],
        "suggested_body": template["body"],
        "detected_language": lang
    }