import unittest
from podbro.generator.claude import ClaudeGenerator
from unittest.mock import patch , Mock
import os


class TestClaudeGenerator(unittest.TestCase):
    @patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test_key'})
    def test_init_with_env_var(self):
        generator = ClaudeGenerator()
        self.assertEqual(generator.model, generator.DEFAULT_MODEL)

    def test_init_without_api_key(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                ClaudeGenerator()

    @patch('podbro.generator.claude.Anthropic')
    def test_generate_podcast_transcript(self, mock_anthropic):
        """Test podcast transcript generation with Claude"""
        mock_client = Mock()
        mock_anthropic.return_value = mock_client

        mock_response = Mock()
        mock_response.content = [Mock(text="Test transcript")]
        mock_client.messages.create.return_value = mock_response

        generator = ClaudeGenerator(api_key="test_key")
        result = generator.generate_podcast_transcript("Test content")

        self.assertEqual(result, "Test transcript")
        mock_client.messages.create.assert_called_once()


