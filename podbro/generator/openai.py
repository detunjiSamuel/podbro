from openai import OpenAI
import os
import logging
from podbro.generator.base import GeneratorBase
from podbro.prompts.base import GEN_POD_SYSTEM_PROMPT


class OpenAIGenerator(GeneratorBase):
    """Generator implementation using OpenAI's API"""

    DEFAULT_MODEL = "gpt-4o"

    def __init__(self, api_key=None, model=None):
        """Initialize OpenAI client

        Args:
            api_key (str, optional): OpenAI API key. Will use environment variable if not provided
            model (str, optional): Model to use for generation. Defaults to gpt-4-turbo-preview
        """
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key must be provided or set in OPENAI_API_KEY environment variable")

        self.client = OpenAI(api_key=api_key)
        self.model = model or self.DEFAULT_MODEL

    def generate_podcast_transcript(self, content):
        """Generate podcast transcript using OpenAI

        Args:
            content (str): Input content to generate podcast from

        Returns:
            str: Generated podcast transcript

        Raises:
            Exception: If generation fails
        """
        try:
            messages = [
                {"role": "system", "content": GEN_POD_SYSTEM_PROMPT},
                {"role": "user", "content": content},
            ]

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )

            return response.choices[0].message.content

        except Exception as e:
            logging.error(f"Error generating transcript with OpenAI: {str(e)}")
            raise e
