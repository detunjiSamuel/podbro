from unittest import TestCase

from main import generate_podcast_transcript_base, parse_transcript


class Test(TestCase):

    def test_generate_podcast_transcript_base(self):
        with (open('./data/sample.txt', "r")) as file:
            content = file.read()
            transcript = generate_podcast_transcript_base(content)
            self.assertIsNotNone(transcript)
            self.assertIsInstance(transcript, str)
            transcript_lower = transcript.lower()
            self.assertTrue(("speaker 1" in transcript_lower) and ("speaker 2" in transcript_lower))

    def test_parse_transcript(self):
        with (open('./data/sample_transcript.txt', "r")) as file:
            content = file.read()
            transcript_arr = parse_transcript(content)
            self.assertIsInstance(transcript_arr, list)
            self.assertTrue(len(transcript_arr) == 22)
            self.assertTrue(all(isinstance(item, tuple) for item in transcript_arr))
