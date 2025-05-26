# Webtoon OCR System

A Python-based system for extracting and translating Korean text from webtoon images using OCR and machine translation.

## Features

- Image splitting into optimal OCR sections
- Korean text recognition using PaddleOCR
- Korean to English translation using Google Translate
- Structured JSON output with word-level translations
- Docker support for easy deployment

## Prerequisites

- Python 3.9 or higher
- Docker (optional, for containerized deployment)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/webtoon-ocr.git
cd webtoon-ocr
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

Basic usage:
```bash
python main.py --input path/to/webtoon.jpg --output path/to/results.json
```

Additional options:
```bash
python main.py --input path/to/webtoon.jpg \
               --output path/to/results.json \
               --tile-size 512 \
               --overlap 64 \
               --verbose
```

### Docker

Build the Docker image:
```bash
docker build -t webtoon-ocr .
```

Run the container:
```bash
docker run -v /host/images:/app/input \
           -v /host/output:/app/output \
           webtoon-ocr \
           --input /app/input/webtoon.jpg \
           --output /app/output/results.json
```

## Output Format

The system generates a JSON file with the following structure:

```json
{
  "timestamp": "2024-03-14T12:00:00.000Z",
  "total_words": 10,
  "results": [
    {
      "word": "내",
      "context": "내 이름은 성진우",
      "translation": "my",
      "confidence": 0.95,
      "position": {
        "x": 100,
        "y": 200
      }
    }
  ]
}
```

## Configuration

The system can be configured through:

1. Environment variables:
   - `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

2. Command line arguments:
   - `--tile-size`: Size of image tiles for OCR
   - `--overlap`: Overlap between tiles in pixels
   - `--verbose`: Enable verbose logging

## Error Handling

The system includes comprehensive error handling for:
- Invalid image formats
- Translation API failures with retry logic
- Memory management for large images
- Logging for debugging and monitoring

## Performance Considerations

- Parallel processing of image tiles
- Translation caching to minimize API calls
- Memory-efficient image handling
- Batch API requests to reduce network overhead

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- PaddleOCR for Korean text recognition
- Google Translate for Korean to English translation
- OpenCV for image processing 