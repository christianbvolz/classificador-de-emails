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

def classify_and_respond(email_content: str) -> dict:
    """
    Orchestrates the flow between NLP cleaning and Groq LLM classification.
    """
    # Step 1: Pre-process text using our NLP pipeline
    cleaned_text, lang = clean_email_text(email_content)

    # Step 2: Define instructions for the AI
    # We use Llama 3, which is excellent at following JSON instructions
    system_prompt = (
    "You are an elite Customer Support AI from a modern financial services company.\n"
    "Your goal is to analyze incoming emails and draft a high-quality response.\n\n"
    
    "CONTEXT FOR THE RESPONSE:\n"
    "1. Tone: Professional, empathetic, and helpful. Use clear and direct language.\n"
    "2. Perspective: Always answer as a member of the company Support Team.\n"
    "3. Resolution: If 'is_productive' is true, acknowledge the specific problem and state that a specialist will investigate immediately.\n\n"

    "OUTPUT RULES:\n"
    "1. 'is_productive': Boolean. True if the user reports a technical bug, payment issue, or request for information. False for casual greetings or spam.\n"
    "2. 'suggested_subject': A professional, organized subject line (e.g., 'Support - [Topic] - Ref: [Reference ID]'). Same language as input.\n"
    "3. 'suggested_body': A complete, professional email body. Include a polite greeting, a personalized acknowledgment of the issue, and a formal closing (e.g., 'Best regards, Support Team'). Same language as input.\n"
    
    "Return strictly JSON with keys: is_productive, suggested_subject, suggested_body."
)

    try:
        # Step 3: Call Groq Cloud API
        # Model 'llama-3.3-70b-versatile' is great for reasoning and JSON accuracy
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Text to analyze:\n\n{cleaned_text}"}
            ],
            response_format={"type": "json_object"},
            temperature=0  # Keeping it deterministic
        )

        ai_data = json.loads(completion.choices[0].message.content)
        
        # Add the detected language to the final response
        ai_data["detected_language"] = lang
        return ai_data

    except Exception as e:
        logger.error(f"Groq service failure: {e}")
        raise LLMServiceError("The AI service is currently unavailable via Groq.")