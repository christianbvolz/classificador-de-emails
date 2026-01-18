"""Utilities for NLP processing: language detection, cleaning, and lemmatization.

This module provides helpers used by the API to detect language, clean, and
lemmatize email text using spaCy.
"""

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
    """Load a spaCy model for the requested language.

    Args:
        lang (str): ISO language code (e.g. 'pt' or 'en').

    Returns:
        The loaded spaCy language model instance, or ``None`` if the language
        is not supported by this service.

    Raises:
        NLPProcessingError: If the language is supported but the spaCy model
            package is not installed or cannot be loaded in the runtime.
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
    """Clean and lemmatize email text.

    The pipeline performs regex-based noise removal (HTML tags, URLs,
    and email addresses), attempts to detect the text language, and when a
    corresponding spaCy model is available, lemmatizes and filters tokens
    (removing stop words, punctuation and spaces).

    Args:
        text (str): Raw email text to process.

    Returns:
        tuple[str, str]: A pair ``(cleaned_text, detected_language)`` where
        ``cleaned_text`` is the processed, lowercased, token-joined string and
        ``detected_language`` is the ISO code detected (e.g. 'pt' or 'en').

    Raises:
        NLPProcessingError: For unexpected errors during processing.
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
