import edge_tts
from edge_tts import VoicesManager

import asyncio

from pydub import AudioSegment


async def run_all_pending_tasks(pending_tasks):
    """
    Run all pending tasks
    :param pending_tasks:
    :return:
    """
    await asyncio.gather(*pending_tasks)


class EdgeSpeech:
    def __init__(self):
        self.voices = []
        self.voices_manager = None

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
        voices = self.get_voices()
        matched_voices = {}

        idx = 0
        count = 0
        pending_tasks = []

        for speaker, dialogue in transcript_arr:

            if speaker not in matched_voices:
                if idx >= len(voices):
                    raise Exception("No more voices available")
                matched_voices[speaker] = voices[idx]
                idx += 1

            async def _generate(text, voice, file_name):
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save(file_name)

            pending_tasks.append(
                _generate(dialogue,
                          matched_voices[speaker],
                          f"edge_output{count}.wav")
            )
            count += 1

            if count > 2:
                break

        asyncio.run(run_all_pending_tasks(pending_tasks))

        audio_result = [f"edge_output{count}.wav" for count in range(count)]
        audio_final = None
        for audio in audio_result:
            print(audio)
            if audio_final is None:
                audio_final = AudioSegment.from_file(audio)
            else:
                audio_final += AudioSegment.from_file(audio)

        audio_final.export("final_edge.wav", format="wav")

        return audio_final
