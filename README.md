# PodBro

PodBro is a Python-based tool that generates podcasts from various content sources including YouTube videos, web pages, PDFs, and audio/video files. It uses OpenAI's APIs for content processing and text-to-speech conversion.

## Features

- Multi-source content extraction from:
  - YouTube videos (with transcript support)
  - Web pages and articles
  - PDF documents
  - Audio/video files
- Text-to-speech conversion using:
  - Microsoft Edge TTS
  - OpenAI TTS
- Automatic content processing and podcast script generation
- Support for multiple voices in generated podcasts

## Installation

```bash
# Clone the repository
git clone https://github.com/detunjisamuel/lo.git

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export OPENAI_API_KEY=your_api_key
```

## Usage

### Command Line Interface

```bash
# Basic usage with a YouTube URL
python -m podbro.main create --url "https://www.youtube.com/watch?v=example"

# Combine multiple sources
python -m podbro.main create \
    --url "https://www.youtube.com/watch?v=example" \
    --file "presentation.pdf" \
    --text "Additional content to include" \
    --tts-model edge
```

### Python API

```python
from podbro.main import PodcastGenerator, TTSModel

# Initialize generator
generator = PodcastGenerator()

# Create podcast from multiple sources
result_file = generator.create_podcast(
    urls=["https://www.youtube.com/watch?v=example"],
    files=["document.pdf"],
    text="Additional content",
    tts_model=TTSModel.EDGE
)
```

## Sample Output

Here's a workflow example:

1. Input: YouTube video about AI advances
2. Content extraction:
```python
# Extract content from YouTube
youtube_parser = YouTube("https://www.youtube.com/watch?v=example")
content = youtube_parser.extract_content_from_source()
```

3. Generate podcast script:
```python
# Process content and generate script
transcript = generate_podcast_transcript(content)

# Sample output:
"""
Speaker 1: Welcome to today's episode about artificial intelligence...
Speaker 2: That's fascinating! Could you tell us more about...
"""
```

4. Convert to audio using Edge TTS or OpenAI TTS

## Testing

```bash
# Run all tests
python -m unittest discover tests

# Run specific test case
python -m unittest tests.test_main.TestPodcastGenerator
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.