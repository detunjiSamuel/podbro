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

from content_parsers.media import transcribe_audio_file, download_audio_file

from content_parsers.webpage import is_valid_url

from content_parsers.pdf import file_exists, Pdf
from content_parsers.youtube import YouTube
from content_parsers.media import Media
from content_parsers.webpage import WebPage

from generator.base import generate_podcast_transcript, parse_transcript

from tts.edge import EdgeSpeech

import logging


# TODO: Add cleanup method to remove unwanted files
# Similar to Teardown in tests
# TODO : make is valid source in base a static method or class method


def speech_to_text():
    # big files should be handled

    audio_file_path = download_audio_file("https://www.youtube.com/watch?v=VzJG4IpYDvs")
    transcript = transcribe_audio_file(audio_file_path)

    return transcript


def determine_content_parser_for_files(file_path):
    raise "Not Implemented : need to adjust is valid source and test"
    # order is important
    content_parsers = (
        Pdf,
        Media,
    )

    for content_parser in content_parsers:
        if content_parser.is_valid_source(file_path):
            return content_parser(file_path)

    logging.error(f"No content parser found for the file:{file_path}")
    raise Exception("No content parser found for the file")


def determine_content_parser_for_urls(url):
    raise "Not Implemented : need to adjust is valid source and test"
    # order is important
    content_parsers = (
        YouTube,
        Media,
        WebPage
    )

    for content_parser in content_parsers:
        if content_parser.is_valid_source(url):
            return content_parser(url)

    logging.error(f"No content parser found for the url:{url}")
    raise Exception("No content parser found for the url")


def create_podcast(
        urls,  # webpages , video links  , regular youtube links ,  audio
        text,  #
        files  # audio , video , pdfs
):
    # validate weblinks
    for url in urls:
        if not is_valid_url(url):
            raise Exception("Invalid URL")

    for file in files:
        if not file_exists(file):
            raise Exception("Invalid FILE PATH")

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
    transcript_arr = parse_transcript(transcript)

    speech = EdgeSpeech()
    _, result_file_path = speech.generate_audio_content(transcript_arr)

    return result_file_path


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
