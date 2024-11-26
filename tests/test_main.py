from unittest import TestCase

from pydub import AudioSegment
from main import extract_text_from_pdf, generate_podcast_transcript_base, generate_audio_content, parse_transcript


class Test(TestCase):
    def test_extract_text_from_pdf(self):
        max_content_length = 50000
        pdf_path = "./data/sample.pdf"
        content = extract_text_from_pdf(pdf_path, max_content_length)

        self.assertIsNotNone(content)
        self.assertIsInstance(content, str)

        with open('./data/sample.txt', "r") as file:
            self.assertEqual(content[:max_content_length], file.read()[:max_content_length])

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

    def test_generate_audio_content(self):
        with (open('./data/sample_transcript.txt', "r")) as file:
            content = file.read().lower()
            transcript_arr = parse_transcript(content)[:5]
            audio_segments_merged = generate_audio_content(transcript_arr)

            self.assertIsInstance(audio_segments_merged, AudioSegment)