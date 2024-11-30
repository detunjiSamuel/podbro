from unittest import TestCase

from speech.tts import EdgeSpeech

from main import parse_transcript, generate_audio_content

from pydub import AudioSegment


class SpeechBaseCase(TestCase):
    def setUp(self):
        with (open('./data/sample_transcript.txt', "r")) as file:
            self.content = file.read()
        self.transcript_arr = parse_transcript(self.content)

    def test_generate_audio_content(self):
        audio_segments_merged = self.generate_audio_content(self.transcript_arr)
        self.assertIsInstance(audio_segments_merged, AudioSegment)

    def generate_audio_content(self, transcript_arr):
        raise NotImplementedError("Subclasses must implement `generate_audio_content`.")


class TestOpenAISpeech(SpeechBaseCase):

    def setUp(self):
        super().setUp()
        self.generate_audio_content = generate_audio_content


class TestEdgeSpeech(SpeechBaseCase):
    def setUp(self):
        super().setUp()
        self.generate_audio_content = EdgeSpeech().generate_audio_content
