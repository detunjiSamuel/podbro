# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


"""

App Goals:

 Use LLam exclusively if it is the fastest

 Tooling to be used by existing podscaster
  Assist in transcription and podcast notes

 Gen Podcast from content_parsers
  Convert knowledge in form of links , papers or videos and generate interactive content_parsers from it

App Features:

Expected MVP:

# Extract text from PDF
# Suggested - Cleanup pdf text using regex o just feed into LLM

"""

from typing import List, Optional
import typer

from podbro.content_parsers.webpage import is_valid_url

from podbro.content_parsers.pdf import file_exists, Pdf
from podbro.content_parsers.youtube import YouTube
from podbro.content_parsers.media import Media
from podbro.content_parsers.webpage import WebPage

from podbro.generator.base import parse_transcript, generate_podcast_transcript

from podbro.tts.edge import EdgeSpeech
from podbro.tts.openai import OpenAISpeech

import logging
from enum import Enum
from functools import lru_cache

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TTSModel(str, Enum):
    EDGE = "edge"
    OPENAI = "openai"


class ContentParser:
    @classmethod
    def validate_sources(cls, urls: List[str], files: List[str]) -> None:
        for url in urls:
            if not is_valid_url(url):
                raise ValueError(f"Invalid URL: {url}")

        for file in files:
            if not file_exists(file):
                raise ValueError(f"Invalid file path: {file}")

    @staticmethod
    @lru_cache(maxsize=None)
    def get_parser_mapping():
        return {
            # The order is important
            'url': [YouTube, Media, WebPage],
            'file': [Pdf, Media]
        }

    @classmethod
    def get_appropriate_parser(cls, source: str, source_type: str):
        parsers = cls.get_parser_mapping()[source_type]

        for parser in parsers:
            try:
                if parser.validate_source(source):
                    return parser(source)
            except Exception as e:
                logger.debug(f"Parser {parser.__name__} failed for {source}: {str(e)}")
                continue

        raise ValueError(f"No suitable content parser found for: {source}")


class PodcastGenerator:

    def __init__(self):
        self._tts_models = {
            TTSModel.EDGE: EdgeSpeech,
            TTSModel.OPENAI: OpenAISpeech,
        }

    @lru_cache(maxsize=None)
    def get_tts_model(self, model_name: TTSModel):
        """Get TTS model instance with caching"""
        tts_model_class = self._tts_models.get(model_name)
        if not tts_model_class:
            raise ValueError(f"Unsupported TTS model: {model_name}")
        return tts_model_class()

    def extract_content(self,
                        urls: List[str],
                        files: List[str],
                        text: Optional[str]) -> str:
        ContentParser.validate_sources(urls, files)

        content = []
        if text:
            content.append(text)

        # Process URLs
        for url in urls:
            parser = ContentParser.get_appropriate_parser(url, 'url')
            content.append(parser.extract_content_from_source())

        # Process files
        for file in files:
            parser = ContentParser.get_appropriate_parser(file, 'file')
            content.append(parser.extract_content_from_source())

        return " ".join(content)

    def create_podcast(
            self,
            urls: List[str] = None,
            text: Optional[str] = None,
            files: List[str] = None,
            content_model: str = "openai",
            tts_model: TTSModel = TTSModel.EDGE,
    ) -> str:
        """
        Create a podcast from various content sources

        Args:
            urls: List of URLs (web pages, videos, etc.)
            text: Direct text input
            files: List of file paths (audio, video, PDFs)
            content_model: Model for content processing
            tts_model: Text-to-speech model to use

        Returns:
            str: Path to the generated audio file
        """
        urls = urls or []
        files = files or []

        try:
            # Extract and process content
            content = self.extract_content(urls, files, text)

            # Generate transcript
            transcript = generate_podcast_transcript(content)
            transcript_arr = parse_transcript(transcript)

            # Generate audio
            speech = self.get_tts_model(tts_model)
            _, result_file_path = speech.generate_audio_content(transcript_arr)

            return result_file_path

        except Exception as e:
            logger.error(f"Failed to create podcast: {str(e)}")
            raise


# CLI implementation
app = typer.Typer()

@app.command()
def create(
    urls: List[str] = typer.Option(None, "--url", "-u", help="URLs to process"),
    text: str = typer.Option(None, "--text", "-t", help="Direct text input"),
    files: List[str] = typer.Option(None, "--file", "-f", help="Files to process"),
    content_model: str = typer.Option("openai", "--content-model", "-c", help="Content processing model"),
    tts_model: TTSModel = typer.Option(TTSModel.EDGE, "--tts-model", "-m", help="Text-to-speech model")
) -> None:
    """Create a podcast from various content sources"""
    try:
        generator = PodcastGenerator()
        result = generator.create_podcast(
            urls=urls,
            text=text,
            files=files,
            content_model=content_model,
            tts_model=tts_model
        )
        typer.echo(f"Podcast created successfully: {result}")
    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)




@lru_cache(maxsize=None)
def get_content_parser_mapping():
    return {
        'url': [YouTube, Media, WebPage],
        'file': [Pdf, Media]
    }


def get_content_parser(source: str, source_type: str):
    parsers = get_content_parser_mapping()[source_type]

    for parser in parsers:
        if parser.validate_source(source):
            return parser(source)

    logging.error(f"No content parser found :{source}")
    raise Exception(f"No content parser found :{source}")


def extract_content(urls, files, text):
    # validate weblinks
    for url in urls:
        if not is_valid_url(url):
            raise Exception(f"Invalid URL : {url}")

    for file in files:
        if not file_exists(file):
            raise Exception(f"Invalid FILE PATH :{file}")

    content = []
    if text:
        content.append(text)

    for url in urls:
        content_parser = get_content_parser(url, 'url')
        content.append(content_parser.extract_content_from_source())

    for file in files:
        content_parser = get_content_parser(file, 'file')
        content.append(content_parser.extract_content_from_source())

    transcript = " ".join(content)
    return transcript


@lru_cache(maxsize=None)
def get_tts_model(model_name):
    tts_models = {
        TTSModel.EDGE: EdgeSpeech,
        TTSModel.OPENAI: OpenAISpeech,
    }

    tts_model = tts_models.get(model_name)
    if not tts_model:
        raise Exception(f"No TTS model found for the model name:{model_name}")

    return tts_model()


def create_podcast(
        urls,  # webpages , video links  , regular youtube links ,  audio
        text,  #
        files,  # audio , video , pdfs
        content_model,  # openai ,
        tts_model=None,  # edge , openai
):
    content = extract_content(urls, files, text)

    transcript = generate_podcast_transcript(content)
    transcript_arr = parse_transcript(transcript)

    speech = get_tts_model(tts_model)
    _, result_file_path = speech.generate_audio_content(transcript_arr)

    return result_file_path


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    app()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
