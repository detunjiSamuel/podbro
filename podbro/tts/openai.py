import datetime

from openai import OpenAI

from podbro.tts.base import merge_audio_files, clean_up_segments_files, SpeechBase

import os
import uuid


class OpenAISpeech(SpeechBase):
    voices = (
        "alloy", "echo", "fable", "onyx", "nova", "shimmer"
    )

    def __init__(self):

        if not os.getenv("OPENAI_API_KEY"):
            raise Exception("OpenAI API Key not found")

        self.client = OpenAI()

        self.audio_segments = []

    def generate_audio_content(self, transcript_arr):
        """
        Generate audio content_parsers from the transcript Array
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
            file_name = f'edge_output{uuid.uuid4()}.wav'
            response = self.client.audio.speech.create(
                model="tts-1",
                voice=matched_voices[speaker],
                input=dialogue
            )
            response.stream_to_file(file_name)
            self.audio_segments.append(file_name)
        audio_file_path = f"final_edge{uuid.uuid4()}.wav"
        audio_final = merge_audio_files(self.audio_segments, audio_file_path)
        clean_up_segments_files(self.audio_segments)
        return audio_final, audio_file_path  # audiosegment , file_path
