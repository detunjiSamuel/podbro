import logging

import os

import asyncio

from pydub import AudioSegment


async def run_all_pending_tasks(pending_tasks):
    """
    Run all pending tasks
    :param pending_tasks:
    :return:
    """
    await asyncio.gather(*pending_tasks)


def clean_up_segments_files(audio_files):
    """
    Delete unused audio segments files
    :param audio_files: list
    :return:

    """
    for audio in audio_files:
        if os.path.exists(audio):
            os.remove(audio)


def merge_audio_files(audio_files, output_file_path):
    """
    Merge audio segments to single audio file
    :param audio_files: list
    :param output_file_path: str
    :return: AudioSegment
    """
    try:

        if not audio_files:
            raise ValueError("No audio segments to merge")

        audio_final = None
        for audio in audio_files:
            if not os.path.exists(audio):
                raise FileNotFoundError(f"File {audio} not found")
            if audio_final is None:
                audio_final = AudioSegment.from_file(audio)
            else:
                audio_final += AudioSegment.from_file(audio)
        if output_file_path:
            _ = audio_final.export(output_file_path, format="wav")
            _.close()  # frees up resources
        return audio_final
    except Exception as e:
        logging.error(e)
        raise


