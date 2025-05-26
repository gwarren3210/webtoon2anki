from paddleocr import PaddleOCR
import numpy as np
from typing import List, Dict, Any
import logging
from config.config import PADDLEOCR_CONFIG

logger = logging.getLogger(__name__)

class OCREngine:
    def __init__(self):
        """Initialize PaddleOCR with Korean language support."""
        try:
            self.ocr = PaddleOCR(**PADDLEOCR_CONFIG)
            logger.info("PaddleOCR initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize PaddleOCR: {str(e)}")
            raise

    def process_tile(self, tile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Process a single tile and extract text with coordinates.
        Returns a list of dictionaries containing text and its coordinates.
        """
        try:
            # Get OCR results
            result = self.ocr.ocr(tile['image'], cls=True)
            
            if not result or not result[0]:
                return []

            # Process results
            text_results = []
            for line in result[0]:
                points, (text, confidence) = line
                
                # Convert points to absolute coordinates
                x1, y1 = tile['coordinates']['x1'], tile['coordinates']['y1']
                abs_points = [[p[0] + x1, p[1] + y1] for p in points]
                
                text_results.append({
                    'text': text,
                    'confidence': float(confidence),
                    'points': abs_points,
                    'bbox': {
                        'x1': min(p[0] for p in abs_points),
                        'y1': min(p[1] for p in abs_points),
                        'x2': max(p[0] for p in abs_points),
                        'y2': max(p[1] for p in abs_points)
                    }
                })

            return text_results

        except Exception as e:
            logger.error(f"Error processing tile: {str(e)}")
            return []

    def deduplicate_text(self, text_results: List[Dict[str, Any]], 
                        overlap_threshold: float = 0.5) -> List[Dict[str, Any]]:
        """
        Remove duplicate text from overlapping regions.
        Uses IoU (Intersection over Union) to determine overlapping text.
        """
        if not text_results:
            return []

        def calculate_iou(box1: Dict[str, float], box2: Dict[str, float]) -> float:
            """Calculate IoU between two bounding boxes."""
            x1 = max(box1['x1'], box2['x1'])
            y1 = max(box1['y1'], box2['y1'])
            x2 = min(box1['x2'], box2['x2'])
            y2 = min(box1['y2'], box2['y2'])

            intersection = max(0, x2 - x1) * max(0, y2 - y1)
            box1_area = (box1['x2'] - box1['x1']) * (box1['y2'] - box1['y1'])
            box2_area = (box2['x2'] - box2['x1']) * (box2['y2'] - box2['y1'])
            union = box1_area + box2_area - intersection

            return intersection / union if union > 0 else 0

        # Sort by confidence
        sorted_results = sorted(text_results, key=lambda x: x['confidence'], reverse=True)
        unique_results = []

        for result in sorted_results:
            is_duplicate = False
            for unique_result in unique_results:
                iou = calculate_iou(result['bbox'], unique_result['bbox'])
                if iou > overlap_threshold:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_results.append(result)

        return unique_results

    def process_image(self, tiles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process all tiles and combine results.
        Returns a list of unique text detections with their coordinates.
        """
        all_results = []
        
        for tile in tiles:
            tile_results = self.process_tile(tile)
            all_results.extend(tile_results)
        
        # Deduplicate results
        unique_results = self.deduplicate_text(all_results)
        logger.info(f"Found {len(unique_results)} unique text regions")
        
        return unique_results 