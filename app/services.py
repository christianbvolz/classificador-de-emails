import os
import json
import logging
from groq import Groq
from dotenv import load_dotenv
from .utils import clean_email_text
from .exceptions import LLMServiceError

load_dotenv()

# Initialize the Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
logger = logging.getLogger(__name__)

# Response templates for fallback scenarios
RESPONSE_TEMPLATES = {
    "pt": {
        "productive": {
            "subject": "Re: Sua solicitação - Suporte Técnico",
            "body": "Prezado(a) cliente,\n\nRecebemos sua solicitação e nossa equipe já iniciou a análise do caso. "
                   "Um especialista entrará em contato em breve com mais informações.\n\n"
                   "Agradecemos pela compreensão.\n\nAtenciosamente,\nEquipe de Suporte"
        },
        "unproductive": {
            "subject": "Re: Sua mensagem",
            "body": "Olá,\n\nAgradecemos pelo contato!\n\n"
                   "Atenciosamente,\nEquipe de Suporte"
        }
    },
    "en": {
        "productive": {
            "subject": "Re: Your Request - Technical Support",
            "body": "Dear customer,\n\nWe have received your request and our team has already started analyzing your case. "
                   "A specialist will contact you shortly with more information.\n\n"
                   "Thank you for your understanding.\n\nBest regards,\nSupport Team"
        },
        "unproductive": {
            "subject": "Re: Your Message",
            "body": "Hello,\n\nThank you for reaching out!\n\n"
                   "Best regards,\nSupport Team"
        }
    }
}

def classify_and_respond(email_content: str) -> dict:
    """
    Orchestrates the flow between NLP cleaning and Groq LLM classification.
    Makes a single LLM call and falls back to a template when needed.

    Args:
        email_content: Raw email text to classify and respond to

    Returns:
        dict with is_productive, suggested_subject, suggested_body, detected_language
    """
    # Step 1: Pre-process text using our NLP pipeline
    cleaned_text, lang = clean_email_text(email_content)

    # Step 2: Enhanced prompt with few-shot examples from templates
    examples_text = "EXAMPLES:\n"
    for lang_code, categories in RESPONSE_TEMPLATES.items():
        lang_name = "Portuguese" if lang_code == "pt" else "English"
        for category_type, template in categories.items():
            is_prod = category_type == "productive"
            examples_text += f"Example ({category_type.title()} - {lang_name}):\n"
            examples_text += f"Output: {{\"is_productive\": {str(is_prod).lower()}, "
            examples_text += f"\"suggested_subject\": \"{template['subject']}\", "
            examples_text += f"\"suggested_body\": \"{template['body']}\"}}\n\n"
    
    system_prompt = (
    "You are an elite Customer Support AI from a modern financial services company.\n"
    "Your goal is to analyze incoming emails and draft a high-quality response.\n\n"
    
    "CONTEXT FOR THE RESPONSE:\n"
    "1. Category identification: First identify the category (payment_issue, technical_support, information_request, greeting, complaint, or spam) and use this to craft a more appropriate response.\n"
    "2. Use of texts: Use the CLEANED text (lemmatized) to perform analysis, intent extraction and classification. Use the ORIGINAL email only to personalize the suggested subject and body (names, reference numbers, quoted phrases). Do NOT use the original raw text for classification decisions.\n"
    "3. Perspective: Always answer as a member of the company Support Team.\n"
    "4. Tone: Professional, empathetic, and helpful. Use clear and direct language.\n"
    "5. Personalization: Reference specific details from the customer's email when possible, taking them from the original text but applying privacy-aware redaction if sensitive.\n"
    "6. Structure: Use 3 paragraphs - greeting, main content with personalized details, formal closing.\n"
    "7. Length: Keep body between 100-250 words for clarity.\n\n"

    "OUTPUT RULES:\n"
    "1. 'is_productive': Boolean. True if the user reports a technical bug, payment issue, or request for information. False for casual greetings or spam.\n"
    "2. 'suggested_subject': A professional, organized subject line (e.g., 'Re: [Topic] - Support'). Same language as input.\n"
    "3. 'suggested_body': A complete, professional email body. Include greeting, personalized acknowledgment, next steps, and closing. Same language as input.\n\n"
    
    f"{examples_text}"
    "Return strictly JSON with keys: is_productive, suggested_subject, suggested_body."
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
            max_tokens=800    # Limit response size
        )

        ai_data = json.loads(completion.choices[0].message.content)

        # Validate response quality; if invalid, use fallback template
        if not _validate_response(ai_data):
            logger.warning("Validation failed. Using fallback template.")
            ai_data = _get_fallback_response(lang, ai_data.get("is_productive", True))

        # Add metadata
        ai_data["detected_language"] = lang

        # Log for monitoring and improvements
        logger.info(
            f"Classification complete - Productive: {ai_data.get('is_productive')}, "
            f"Lang: {lang}, "
            f"Tokens: {completion.usage.total_tokens if hasattr(completion, 'usage') else 'N/A'}"
        )

        return ai_data

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return _get_fallback_response(lang, True)

    except Exception as e:
        logger.error(f"Groq service failure: {e}")
        raise LLMServiceError("The AI service is currently unavailable via Groq.")


def _validate_response(ai_data: dict) -> bool:
    """
    Validates that the AI response meets minimum quality standards.
    
    Args:
        ai_data: The parsed JSON response from the LLM
        
    Returns:
        True if valid, False otherwise
    """
    # Check required fields
    required_fields = ["is_productive", "suggested_subject", "suggested_body"]
    if not all(field in ai_data for field in required_fields):
        return False
    
    # Check minimum content length
    if len(ai_data.get("suggested_body", "")) < 50:
        return False
    
    if len(ai_data.get("suggested_subject", "")) < 5:
        return False
    
    return True


def _get_fallback_response(lang: str, is_productive: bool) -> dict:
    """
    Returns a template-based fallback response when AI generation fails.
    
    Args:
        lang: Detected language code
        is_productive: Whether the email is productive
        
    Returns:
        dict with fallback response data
    """
    # Default to Portuguese if language not in templates
    template_lang = lang if lang in RESPONSE_TEMPLATES else "pt"
    template_type = "productive" if is_productive else "unproductive"
    
    template = RESPONSE_TEMPLATES[template_lang][template_type]
    
    return {
        "is_productive": is_productive,
        "suggested_subject": template["subject"],
        "suggested_body": template["body"],
        "detected_language": lang
    }