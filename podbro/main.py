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

from podbro.content_parsers.media import transcribe_audio_file, download_file

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


def speech_to_text():
    # big files should be handled

    audio_file_path = download_file("https://www.youtube.com/watch?v=VzJG4IpYDvs")
    transcript = transcribe_audio_file(audio_file_path)

    return transcript


def determine_content_parser_for_files(file_path):
    # order is important
    content_parsers = (
        Pdf,
        Media,
    )

    for content_parser in content_parsers:
        if content_parser.validate_source(file_path):
            return content_parser(file_path)

    logging.error(f"No content parser found for the file:{file_path}")
    raise Exception("No content parser found for the file")


def determine_content_parser_for_urls(url):
    # order is important
    content_parsers = (
        YouTube,
        Media,
        WebPage
    )

    for parser in content_parsers:
        if parser.validate_source(url):
            return parser(url)

    logging.error(f"No content parser found for the url:{url}")
    raise Exception("No content parser found for the url")


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
        content_parser = determine_content_parser_for_urls(url)
        content.append(content_parser.extract_content_from_source())

    for files in files:
        content_parser = determine_content_parser_for_files(files)
        content.append(content_parser.extract_content_from_source())

    transcript = " ".join(content)
    return transcript


class TTSModel(str, Enum):
    EDGE = "edge"
    OPENAI = "openai"


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


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
