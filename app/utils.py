import spacy
import re
from functools import lru_cache
from langdetect import detect, DetectorFactory
from .exceptions import NLPProcessingError

# Ensure language detection is consistent across runs
DetectorFactory.seed = 0

# Module-level constant for supported language models
SUPPORTED_MODELS = {
    "pt": "pt_core_news_sm",
    "en": "en_core_web_sm"
}

@lru_cache(maxsize=2)
def get_spacy_model(lang: str):
    """
    Loads the spaCy model from memory or disk.
    Returns None if no model is supported for the language.
    """
    model_name = SUPPORTED_MODELS.get(lang)
    if not model_name:
        return None

    try:
        return spacy.load(model_name)
    except OSError:
        raise NLPProcessingError(
            f"Model {model_name} not found in the container. Check Dockerfile."
        )

def clean_email_text(text: str) -> tuple[str, str]:
    """
    Main NLP Pipeline: 
    1. Removes noise (HTML, URLs, Emails).
    2. Detects the language.
    3. Lemmatizes the text based on the detected language.
    Returns: (cleaned_text, detected_language)
    """
    try:
        # 1. Regex Cleaning
        text = re.sub(r'<.*?>|http\S+|\S+@\S+', '', text)
        
        # 2. Language Detection
        try:
            lang = detect(text)
        except:
            lang = "pt" # Default to Portuguese if detection fails

        # 3. NLP Lemmatization
        nlp = get_spacy_model(lang)
        if nlp:
            doc = nlp(text)
            # Filter stop words, punctuation and extract lemmas
            tokens = [
                t.lemma_.lower() 
                for t in doc 
                if not t.is_stop and not t.is_punct and not t.is_space
            ]
            return " ".join(tokens), lang
            
        # Fallback if no specific model is available
        return " ".join(text.lower().split()), lang
        
    except Exception as e:
        # Wrap any unexpected errors into our custom NLPProcessingError
        raise NLPProcessingError(str(e))