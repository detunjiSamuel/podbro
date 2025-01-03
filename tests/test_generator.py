from unittest import TestCase
from unittest.mock import patch, Mock

import os

from podbro.generator.base import parse_transcript, generate_podcast_transcript


class Test(TestCase):

    def setUp(self):
        self.sample_txt_path = os.path.join(os.path.dirname(__file__), 'data', 'sample.txt')
        self.sample_transcript_path = os.path.join(os.path.dirname(__file__), 'data', 'sample_transcript.txt')

    @patch('podbro.generator.base.OpenAI')
    def test_generate_podcast_transcript_base(self , mock_openai):

        mock_client = Mock()
        mock_openai.return_value = mock_client

        mock_completion = Mock()
        mock_completion.choices = [Mock(message=Mock(content="Speaker 1: Hello\nSpeaker 2: Hi there"))]
        mock_client.chat.completions.create.return_value = mock_completion

        with (open(self.sample_txt_path, "r")) as file:
            content = file.read()
            transcript = generate_podcast_transcript(content)

            self.assertIsNotNone(transcript)
            self.assertIsInstance(transcript, str)
            transcript_lower = transcript.lower()
            self.assertTrue(("speaker 1" in transcript_lower) and ("speaker 2" in transcript_lower))

            # Verify the mock was called with expected parameters
            # mock_client.chat.completions.create.assert_called_once()
            # call_args = mock_client.chat.completions.create.call_args
            # self.assertEqual(call_args[1]['model'], "gpt-4o")

    def test_parse_transcript(self):
        with (open(self.sample_transcript_path, "r")) as file:
            content = file.read()
            transcript_arr = parse_transcript(content)
            self.assertIsInstance(transcript_arr, list)
            self.assertTrue(len(transcript_arr) == 22)
            self.assertTrue(all(isinstance(item, tuple) for item in transcript_arr))
