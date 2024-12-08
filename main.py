# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


"""

App Goals:

 Use LLam exclusively if it is the fastest

 Tooling to be used by existing podscaster
  Assist in transcription and podcast notes

 Gen Podcast from content
  Convert knowledge in form of links , papers or videos and generate interactive content from it

App Features:

Expected MVP:

# Extract text from PDF
# Suggested - Cleanup pdf text using regex o just feed into LLM

"""

import yt_dlp as youtube_dl

import logging

import json

from openai import OpenAI

from pydub import AudioSegment

import os


def break_audio_file_into_usable_chunks(audio_path):
    """
    :param audio_path: Absolute path to the audio file
    :return:
    """
    ten_minutes = 10 * 60 * 1000
    audio = AudioSegment.from_file(audio_path)
    audio_chunks = []

    if len(audio) <= ten_minutes:
        audio_chunks.append(audio_path)
        logging.info("Audio file is less than 10 minutes")
        return audio_chunks

    directory = os.path.dirname(audio_path)
    file_name = os.path.splitext(os.path.basename(audio_path))[0]

    for i in range(0, len(audio), ten_minutes):
        if i + ten_minutes > len(audio):
            curr_chunk = audio[i: len(audio)]
        else:
            curr_chunk = audio[i: i + ten_minutes]

        curr_file = os.path.join(directory, f"{file_name}_{i}.mp3")
        curr_chunk.export(curr_file, format='mp3')
        audio_chunks.append(curr_file)

    logging.info(f"Audio file split into {len(audio_chunks)} chunks")
    return audio_chunks


def transcribe_audio_file(audio_path):
    result = []
    client = OpenAI()

    audio_to_process = break_audio_file_into_usable_chunks(audio_path)

    for i in audio_to_process:
        audio_file = open(i, "rb")
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        print(transcription.text)
        result.append(transcription.text)

    return " ".join(result)


def download_audio_file(audio_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',

        }],
        'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
        'noplaylist': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        # default output template : %(title)s [%(id)s].%(ext)s.
        info = ydl.extract_info(
            audio_url,
        )
        info = ydl.sanitize_info(info)
        file_path = info["requested_downloads"][0]["filepath"]
        return file_path


def speech_to_text():
    # big files should be handled
    # https://platform.openai.com/docs/guides/speech-to-text#longer-inputs

    audio_file_path = download_audio_file("https://www.youtube.com/watch?v=VzJG4IpYDvs")
    transcript = transcribe_audio_file(audio_file_path)

    return transcript


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
