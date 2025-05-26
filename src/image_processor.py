import cv2
import numpy as np
from PIL import Image
import os
from typing import List, Tuple, Dict
import logging
from config.config import DEFAULT_TILE_SIZE, DEFAULT_OVERLAP, SUPPORTED_FORMATS

logger = logging.getLogger(__name__)

class ImageProcessor:
    def __init__(self, tile_size: int = DEFAULT_TILE_SIZE, overlap: int = DEFAULT_OVERLAP):
        self.tile_size = tile_size
        self.overlap = overlap

    def validate_image(self, image_path: str) -> bool:
        """Validate if the image file exists and is in a supported format."""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        ext = os.path.splitext(image_path)[1].lower()
        if ext not in SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported image format: {ext}. Supported formats: {SUPPORTED_FORMATS}")
        
        return True

    def load_image(self, image_path: str) -> np.ndarray:
        """Load image and convert to RGB format."""
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Failed to load image: {image_path}")
            return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        except Exception as e:
            logger.error(f"Error loading image: {str(e)}")
            raise

    def split_image(self, image: np.ndarray) -> List[Dict[str, any]]:
        """
        Split image into overlapping tiles.
        Returns a list of dictionaries containing tile images and their coordinates.
        """
        height, width = image.shape[:2]
        tiles = []
        
        # Calculate number of tiles needed
        num_tiles_x = (width - self.overlap) // (self.tile_size - self.overlap)
        num_tiles_y = (height - self.overlap) // (self.tile_size - self.overlap)
        
        for y in range(num_tiles_y):
            for x in range(num_tiles_x):
                # Calculate tile coordinates
                x1 = x * (self.tile_size - self.overlap)
                y1 = y * (self.tile_size - self.overlap)
                x2 = min(x1 + self.tile_size, width)
                y2 = min(y1 + self.tile_size, height)
                
                # Extract tile
                tile = image[y1:y2, x1:x2]
                
                # Store tile with its coordinates
                tiles.append({
                    'image': tile,
                    'coordinates': {
                        'x1': x1,
                        'y1': y1,
                        'x2': x2,
                        'y2': y2
                    }
                })
        
        return tiles

    def process_image(self, image_path: str) -> List[Dict[str, any]]:
        """
        Main method to process an image file.
        Returns a list of processed tiles with their coordinates.
        """
        try:
            self.validate_image(image_path)
            image = self.load_image(image_path)
            tiles = self.split_image(image)
            logger.info(f"Successfully split image into {len(tiles)} tiles")
            return tiles
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            raise

    def preprocess_tile(self, tile: np.ndarray) -> np.ndarray:
        """
        Preprocess a tile for better OCR results.
        """
        # Convert to grayscale
        gray = cv2.cvtColor(tile, cv2.COLOR_RGB2GRAY)
        
        # Apply adaptive thresholding
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(binary)
        
        return denoised 