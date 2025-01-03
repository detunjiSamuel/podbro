from unittest import TestCase
from unittest.mock import patch, Mock

from podbro.generator.llama import LlamaGenerator

class TestLlamaGenerator(TestCase):

    @patch('transformers.AutoTokenizer.from_pretrained')
    @patch('transformers.AutoModelForCausalLM.from_pretrained')
    def test_init(self, mock_model, mock_tokenizer):
        generator = LlamaGenerator()
        self.assertEqual(generator.model_name, generator.DEFAULT_MODEL)
        mock_tokenizer.assert_called_once()
        mock_model.assert_called_once()


    @patch('transformers.AutoTokenizer.from_pretrained')
    @patch('transformers.AutoModelForCausalLM.from_pretrained')
    def test_generate_podcast_transcript(self, mock_model, mock_tokenizer):
        mock_tokenizer.return_value = Mock(
            __call__=lambda text, return_tensors: Mock(to=lambda device: {}),
            decode=lambda tokens, skip_special_tokens: "Test transcript"
        )
        mock_model.return_value = Mock(
            generate=lambda **kwargs: [Mock()]
        )

        generator = LlamaGenerator()
        result = generator.generate_podcast_transcript("Test content")

        self.assertTrue("Test transcript" in result)
        mock_tokenizer.assert_called()
        mock_model.assert_called()
