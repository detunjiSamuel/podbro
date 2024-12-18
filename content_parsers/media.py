import logging
import os

import yt_dlp as youtube_dl
from openai import OpenAI
from pydub import AudioSegment

from content_parsers.base import ContentBase
from content_parsers.webpage import is_valid_url
from content_parsers.pdf import file_exists

import subprocess


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

    if len(audio_to_process) > 1:
        # might not be a great idea to delete the original file here
        for i in audio_to_process:
            os.remove(i)

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


def video_to_audio(input_video: str, audio_format: str = "mp3"):
    """
    Converts a video file to an audio file using FFmpeg.

    Parameters:
        input_video (str): Path to the input video file.
        audio_format (str): Desired audio format (e.g., 'mp3', 'aac', 'wav'). Default is 'mp3'.

    Returns:
       Absolute path to the output audio file.
    """

    directory = os.path.dirname(input_video)
    file_name = os.path.splitext(os.path.basename(input_video))[0]
    output_audio = f"{file_name}.{audio_format}"

    try:
        command = [
            "ffmpeg",
            "-i", input_video,  # Input video file
            "-vn",  # Disable video recording
            "-acodec", "libmp3lame" if audio_format == "mp3" else "aac",  # Audio codec based on format
            "-y",  # Overwrite output file without asking
            output_audio  # Output audio file
        ]

        subprocess.run(command, check=True)
        logging.debug(f"Audio successfully extracted to {output_audio}")
        return os.path.join(directory,  output_audio)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error: Failed to convert video to audio. {e}")
    except FileNotFoundError:
        logging.error("Error: FFmpeg not found. Make sure it is installed and added to PATH.")


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

        self.set_source_type()

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

    def extract_content_from_source(self):
        """

        Extract transcript from the audio/Media
        Accepts Both url and file path
        :return:
        """
        if self.source_type == "URL":
            audio_file_path = download_file(self.source)
        elif self.source_type == "VIDEO":
            audio_file_path = video_to_audio(self.source)
        else:
            audio_file_path = self.source
        transcript = transcribe_audio_file(audio_file_path)

        if self.source_type in ["URL", "VIDEO"]:
            os.remove(audio_file_path)
        return transcript
