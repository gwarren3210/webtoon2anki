import json
import os
from typing import List, Dict, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class OutputHandler:
    def __init__(self):
        """Initialize output handler."""
        pass

    def format_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format OCR and translation results into the required output structure.
        """
        formatted_results = []
        
        for result in results:
            # Split text into words (simple space-based splitting for now)
            words = result['text'].split()
            translations = result['translation'].split()
            
            # Ensure we have matching number of words and translations
            min_length = min(len(words), len(translations))
            
            for i in range(min_length):
                formatted_results.append({
                    'word': words[i],
                    'context': result['text'],
                    'translation': translations[i],
                    'confidence': result['confidence'],
                    'position': {
                        'x': result['bbox']['x1'],
                        'y': result['bbox']['y1']
                    }
                })
        
        return formatted_results

    def save_results(self, results: List[Dict[str, Any]], output_path: str) -> str:
        """
        Save results to a JSON file.
        Returns the path to the saved file.
        """
        try:
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Add metadata
            output_data = {
                'timestamp': datetime.now().isoformat(),
                'total_words': len(results),
                'results': results
            }
            
            # Save to file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Results saved to {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")
            raise

    def process_and_save(self, results: List[Dict[str, Any]], output_path: str) -> str:
        """
        Process results and save to file.
        Returns the path to the saved file.
        """
        try:
            formatted_results = self.format_results(results)
            return self.save_results(formatted_results, output_path)
        except Exception as e:
            logger.error(f"Error processing and saving results: {str(e)}")
            raise 