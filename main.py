import argparse
import logging
import os
from src.image_processor import ImageProcessor
from src.ocr_engine import OCREngine
from src.translator import Translator
from src.output_handler import OutputHandler
from config.config import DEFAULT_TILE_SIZE, DEFAULT_OVERLAP, LOG_LEVEL

def setup_logging():
    """Configure logging based on environment settings."""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Webtoon OCR and Translation System')
    
    parser.add_argument('--input', '-i', required=True,
                      help='Path to input webtoon image')
    parser.add_argument('--output', '-o',
                      help='Path to output JSON file (defaults to input directory)')
    parser.add_argument('--tile-size', type=int, default=DEFAULT_TILE_SIZE,
                      help=f'Size of image tiles for OCR (default: {DEFAULT_TILE_SIZE})')
    parser.add_argument('--overlap', type=int, default=DEFAULT_OVERLAP,
                      help=f'Overlap between tiles in pixels (default: {DEFAULT_OVERLAP})')
    parser.add_argument('--verbose', '-v', action='store_true',
                      help='Enable verbose logging')
    
    return parser.parse_args()

def main():
    """Main execution function."""
    # Setup
    setup_logging()
    args = parse_arguments()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Set default output path if not provided
    if not args.output:
        input_dir = os.path.dirname(args.input)
        input_filename = os.path.splitext(os.path.basename(args.input))[0]
        args.output = os.path.join(input_dir, f"{input_filename}_results.json")
    
    try:
        # Initialize components
        image_processor = ImageProcessor(tile_size=args.tile_size, overlap=args.overlap)
        ocr_engine = OCREngine()
        translator = Translator()
        output_handler = OutputHandler()
        
        # Process image
        logging.info(f"Processing image: {args.input}")
        tiles = image_processor.process_image(args.input)
        
        # Perform OCR
        logging.info("Performing OCR on image tiles")
        ocr_results = ocr_engine.process_image(tiles)
        
        # Translate text
        logging.info("Translating detected text")
        translated_results = translator.process_ocr_results(ocr_results)
        
        # Save results
        logging.info(f"Saving results to: {args.output}")
        output_path = output_handler.process_and_save(translated_results, args.output)
        
        logging.info("Processing completed successfully")
        return 0
        
    except Exception as e:
        logging.error(f"Error processing image: {str(e)}")
        return 1

if __name__ == '__main__':
    exit(main()) 