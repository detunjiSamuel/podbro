from unittest import TestCase
import os

from podbro.generator.base import parse_transcript, generate_podcast_transcript


class Test(TestCase):

    def setUp(self):
        self.sample_txt_path = os.path.join(os.path.dirname(__file__), 'data', 'sample.txt')
        self.sample_transcript_path = os.path.join(os.path.dirname(__file__), 'data', 'sample_transcript.txt')

    def test_generate_podcast_transcript_base(self):
        with (open(self.sample_txt_path, "r")) as file:
            content = file.read()
            transcript = generate_podcast_transcript(content)
            self.assertIsNotNone(transcript)
            self.assertIsInstance(transcript, str)
            transcript_lower = transcript.lower()
            self.assertTrue(("speaker 1" in transcript_lower) and ("speaker 2" in transcript_lower))

    def test_parse_transcript(self):
        with (open(self.sample_transcript_path, "r")) as file:
            content = file.read()
            transcript_arr = parse_transcript(content)
            self.assertIsInstance(transcript_arr, list)
            self.assertTrue(len(transcript_arr) == 22)
            self.assertTrue(all(isinstance(item, tuple) for item in transcript_arr))
