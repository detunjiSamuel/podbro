import asyncio
import datetime

import edge_tts
from edge_tts import VoicesManager

from speech.base import run_all_pending_tasks, merge_audio_files, clean_up_segments_files


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
