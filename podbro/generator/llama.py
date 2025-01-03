import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from podbro.generator.base import GeneratorBase

import logging
from podbro.prompts.base import GEN_POD_SYSTEM_PROMPT


class LlamaGenerator(GeneratorBase):
    """Generator implementation using Llama models via Hugging Face"""

    DEFAULT_MODEL = "meta-llama/Llama-3.1-8B-Instruct"

    def __init__(self, model_name=None, device=None):
        """Initialize Llama model and tokenizer

        Args:
            model_name (str): Hugging Face model name/path (default: Llama-2-7b-chat)
            device (str): Device to run model on ('cuda' or 'cpu')
        """
        self.model_name = model_name or self.DEFAULT_MODEL
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')

        try:
            logging.info(f"Loading Llama model {self.model_name} on {self.device}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == 'cuda' else torch.float32,
                device_map="auto"
            )
            logging.info("Model loaded successfully")
        except Exception as e:
            logging.error(f"Error loading Llama model: {str(e)}")
            raise

    def generate_podcast_transcript(self, content):
        """Generate podcast transcript using Llama

        Args:
            content (str): Input content to generate podcast from

        Returns:
            str: Generated podcast transcript
        """
        try:
            # Format prompt with system prompt and content
            prompt = f"{GEN_POD_SYSTEM_PROMPT}\n\nContent: {content}\n\nGenerate podcast transcript:"

            # Tokenize and generate
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=4096,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )

            # Decode and return generated text
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Extract just the generated portion after the prompt
            transcript = generated_text[len(prompt):]
            return transcript.strip()

        except Exception as e:
            logging.error(f"Error generating transcript with Llama: {str(e)}")
            raise