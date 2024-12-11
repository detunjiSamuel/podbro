import logging
import os

import yt_dlp as youtube_dl
from openai import OpenAI
from pydub import AudioSegment

from content_parsers.base import ContentBase
from content_parsers.webpage import is_valid_url
from content_parsers.pdf import file_exists

import youtube_dl


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


def download_file(url, audio=True):
    ydl_opts = {}
    if audio:
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
            url,
        )
        info = ydl.sanitize_info(info)
        file_path = info["requested_downloads"][0]["filepath"]
        return file_path


def download_video_file(url):
    with youtube_dl.YoutubeDL({}) as ydl:
        # default output template : %(title)s [%(id)s].%(ext)s.
        info = ydl.extract_info(
            url,
        )
        info = ydl.sanitize_info(info)
        file_path = info["requested_downloads"][0]["filepath"]
        return file_path


def can_download_from_here(url):
    try:
        with youtube_dl.YoutubeDL({}) as ydl:
            info = ydl.extract_info(
                url,
                download=False
            )
            return True
    except Exception as e:
        return False


class Media(ContentBase):

    def __init__(self, source):
        super().__init__(source)
        self.source_type = None

    @staticmethod
    def is_supported_file_format(file_path):
        audio_extensions = {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"}
        video_extensions = {".mp4", ".avi", ".mkv", ".mov", ".flv", ".wmv", ".webm", ".mpeg", ".3gp"}

        _, ext = os.path.splitext(os.path.basename(file_path))

        if ext in audio_extensions:
            return "AUDIO"
        if ext in video_extensions:
            return "VIDEO"
        logging.error(f"INVALID MEDIA FILE PASSED: {file_path}")
        return False

    @staticmethod
    def validate_source(source):
        if is_valid_url(source) and can_download_from_here(source):
            return True
        return file_exists(source) and Media.is_supported_file_format(source)

    def set_source_type(self):
        if self.is_valid_source():
            if can_download_from_here(self.source):
                self.source_type = "URL"
                return self.source_type
            elif Media.is_supported_file_format(self.source):
                self.source_type = Media.is_supported_file_format(self.source)
                return self.source_type

    def download_video_from_url(self):
        # download the video using ytdl
        # return temp file path

        # might need to use ffmpeg to convert the video to a format that can be used by wispher

        # TODO : check if ydtcl can just auto download the audi
        pass

    def extract_audio_from_video(self):
        # extract audio from the video
        # return the audio file path
        pass

    def extract_content_from_source(self):
        # download the video with ytdl
        # extract the text from the video using wispher
        # return the text
        pass
