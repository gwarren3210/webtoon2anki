import time
from typing import List, Dict, Any
import logging
from googletrans import Translator as GoogleTranslator
from config.config import BATCH_SIZE, MAX_RETRIES, RETRY_DELAY

logger = logging.getLogger(__name__)

class Translator:
    def __init__(self):
        """Initialize translator with Google Translate."""
        self.translator = GoogleTranslator()
        self.cache = {}  # Simple in-memory cache for translations

    def translate_text(self, text: str) -> str:
        """
        Translate a single text string from Korean to English.
        Uses caching to avoid duplicate API calls.
        """
        if text in self.cache:
            return self.cache[text]

        for attempt in range(MAX_RETRIES):
            try:
                result = self.translator.translate(text, src='ko', dest='en')
                translation = result.text
                
                # Cache the result
                self.cache[text] = translation
                return translation
                
            except Exception as e:
                logger.warning(f"Translation attempt {attempt + 1} failed: {str(e)}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                else:
                    logger.error(f"Failed to translate text after {MAX_RETRIES} attempts")
                    return text  # Return original text if translation fails

    def batch_translate(self, texts: List[str]) -> List[str]:
        """
        Translate a batch of texts efficiently.
        Uses batching to minimize API calls.
        """
        translations = []
        
        # Process texts in batches
        for i in range(0, len(texts), BATCH_SIZE):
            batch = texts[i:i + BATCH_SIZE]
            batch_translations = []
            
            for text in batch:
                translation = self.translate_text(text)
                batch_translations.append(translation)
            
            translations.extend(batch_translations)
            
            # Add delay between batches to respect API rate limits
            if i + BATCH_SIZE < len(texts):
                time.sleep(RETRY_DELAY)
        
        return translations

    def process_ocr_results(self, ocr_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process OCR results and add translations.
        Returns a list of dictionaries containing original text, translation, and metadata.
        """
        # Extract unique texts
        texts = list(set(result['text'] for result in ocr_results))
        
        # Get translations
        translations = self.batch_translate(texts)
        
        # Create translation mapping
        translation_map = dict(zip(texts, translations))
        
        # Add translations to results
        for result in ocr_results:
            result['translation'] = translation_map[result['text']]
        
        return ocr_results 