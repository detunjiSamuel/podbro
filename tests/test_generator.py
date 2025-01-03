from unittest import TestCase
from unittest.mock import patch, Mock

import os
from parameterized import parameterized


from podbro.generator.base import parse_transcript, generate_podcast_transcript
from podbro.generator.base import get_generator, ModelProvider

from podbro.generator.openai import OpenAIGenerator
from podbro.generator.claude import ClaudeGenerator
from podbro.generator.llama import LlamaGenerator



class Test(TestCase):

    def setUp(self):
        self.sample_txt_path = os.path.join(os.path.dirname(__file__), 'data', 'sample.txt')
        self.sample_transcript_path = os.path.join(os.path.dirname(__file__), 'data', 'sample_transcript.txt')

    @patch('podbro.generator.openai.OpenAI')
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


class TestGeneratorBase(TestCase):
    """Test cases for base generator functionality"""

    def setUp(self):
        self.sample_txt_path = os.path.join(os.path.dirname(__file__), 'data', 'sample.txt')
        self.sample_transcript_path = os.path.join(os.path.dirname(__file__), 'data', 'sample_transcript.txt')

    def test_parse_transcript(self):
        """Test transcript parsing functionality"""
        with open(self.sample_transcript_path, "r") as file:
            content = file.read()
            transcript_arr = parse_transcript(content)
            self.assertIsInstance(transcript_arr, list)
            self.assertTrue(len(transcript_arr) == 22)
            self.assertTrue(all(isinstance(item, tuple) for item in transcript_arr))

    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    @patch('podbro.generator.openai.OpenAI')
    def test_generate_podcast_transcript_base(self, mock_openai):
        """Test basic podcast transcript generation"""
        mock_client = Mock()
        mock_openai.return_value = mock_client

        mock_completion = Mock()
        mock_completion.choices = [Mock(message=Mock(content="Speaker 1: Hello\nSpeaker 2: Hi there"))]
        mock_client.chat.completions.create.return_value = mock_completion

        with open(self.sample_txt_path, "r") as file:
            content = file.read()
            transcript = generate_podcast_transcript(content)

            self.assertIsNotNone(transcript)
            self.assertIsInstance(transcript, str)
            transcript_lower = transcript.lower()
            self.assertTrue(("speaker 1" in transcript_lower) and ("speaker 2" in transcript_lower))

    @parameterized.expand([
        (ModelProvider.OPENAI, OpenAIGenerator),
        (ModelProvider.CLAUDE, ClaudeGenerator),
        (ModelProvider.LLAMA, LlamaGenerator),
    ])
    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test_key',
        'ANTHROPIC_API_KEY': 'test_key'
    })
    def test_get_generator(self, provider, expected_class):
        """Test generator factory function"""
        generator = get_generator(provider)
        self.assertIsInstance(generator, expected_class)

    def test_get_generator_invalid(self):
        """Test generator factory with invalid provider"""
        with self.assertRaises(ValueError):
            get_generator("invalid_provider")


class TestOpenAIGenerator(TestCase):
    """Test cases for OpenAI generator implementation"""

    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'})
    def test_init_with_env_var(self):
        """Test initialization with environment variable"""
        generator = OpenAIGenerator()
        self.assertEqual(generator.model, generator.DEFAULT_MODEL)

    def test_init_without_api_key(self):
        """Test initialization without API key"""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                OpenAIGenerator()

    @patch('podbro.generator.openai.OpenAI')
    def test_generate_podcast_transcript(self, mock_openai):
        mock_client = Mock()
        mock_openai.return_value = mock_client

        mock_completion = Mock()
        mock_completion.choices = [Mock(message=Mock(content="Test transcript"))]
        mock_client.chat.completions.create.return_value = mock_completion

        generator = OpenAIGenerator(api_key="test_key")
        result = generator.generate_podcast_transcript("Test content")

        self.assertEqual(result, "Test transcript")
        mock_client.chat.completions.create.assert_called_once()
