import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Image Processing Configuration
DEFAULT_TILE_SIZE = 512
DEFAULT_OVERLAP = 64
SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']

# PaddleOCR Configuration
PADDLEOCR_CONFIG = {
    'use_angle_cls': True,
    'lang': 'korean',
    'show_log': False,
    'use_gpu': False  # Set to True if GPU is available
}

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Translation Configuration
BATCH_SIZE = 10  # Number of texts to translate in one API call
MAX_RETRIES = 3  # Maximum number of retries for API calls
RETRY_DELAY = 1  # Delay between retries in seconds 