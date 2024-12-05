import logging

import edge_tts
import os
from edge_tts import VoicesManager

import asyncio

from openai import OpenAI
from pydub import AudioSegment
import datetime


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


class EdgeSpeech:
    def __init__(self):
        super().__init__()
        self.voices = []
        self.voices_manager = None
        self.audio_segments = []

    async def fetch_voices(self):
        """
        Fetch voices used in Microsoft Edge TTS API
        :return list:
        """
        if not self.voices_manager:
            self.voices_manager = await VoicesManager.create()
        voices = self.voices_manager.find(Language="en")
        self.voices = [v["Name"] for v in voices]
        return self.voices

    def get_voices(self):
        if self.voices:
            return self.voices

        self.voices = asyncio.run(self.fetch_voices())
        return self.voices

    def generate_audio_content(self, transcript_arr):
        """
        Generate audio content from the transcript Array
        :param transcript_arr:
        :return: AudioSegment , file_path
        """
        voices = self.get_voices()
        matched_voices = {}

        idx = 0
        pending_tasks = []

        for speaker, dialogue in transcript_arr:

            if speaker not in matched_voices:
                if idx >= len(voices):
                    raise Exception("No more voices available")
                matched_voices[speaker] = voices[idx]
                idx += 1

            async def _generate(text, voice, output_file_name):
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save(output_file_name)

            file_name = f'edge_output{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.wav'
            pending_tasks.append(
                _generate(dialogue,
                          matched_voices[speaker],
                          file_name)
            )

            self.audio_segments.append(file_name)

        asyncio.run(run_all_pending_tasks(pending_tasks))

        audio_file_path = f"final_edge{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"

        audio_final = merge_audio_files(self.audio_segments, audio_file_path)

        clean_up_segments_files(self.audio_segments)

        return audio_final, audio_file_path  # audiosegment , file_path


class OpenAISpeech:
    voices = (
        "alloy", "echo", "fable", "onyx", "nova", "shimmer"
    )

    def __init__(self):
        self.client = OpenAI()

        self.audio_segments = []


    def generate_audio_content(self, transcript_arr):
        """
        Generate audio content from the transcript Array
        :param transcript_arr:
        :return: AudioSegment , file_path
        """
        idx = 0
        matched_voices = {}
        for speaker, dialogue in transcript_arr:
            if speaker not in matched_voices:
                if idx >= len(OpenAISpeech.voices):
                    raise Exception("No more voices available")
                matched_voices[speaker] = OpenAISpeech.voices[idx]
                idx += 1
            file_name = f'edge_output{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.wav'
            response = self.client.audio.speech.create(
                model="tts-1",
                voice=matched_voices[speaker],
                input=dialogue
            )
            response.stream_to_file(file_name)
            self.audio_segments.append(file_name)
        audio_file_path = f"final_edge{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        audio_final = merge_audio_files(self.audio_segments, audio_file_path)
        clean_up_segments_files(self.audio_segments)
        return audio_final, audio_file_path  # audiosegment , file_path

