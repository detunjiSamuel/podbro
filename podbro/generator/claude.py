from anthropic import Anthropic
from podbro.prompts.base import GEN_POD_SYSTEM_PROMPT
from podbro.generator.base import GeneratorBase

import os

import logging


class ClaudeGenerator(GeneratorBase):
    """Generator implementation using Anthropic's Claude API"""

    DEFAULT_MODEL = "claude-3-5-sonnet-20241022"

    def __init__(self, api_key=None , model=None):
        if not api_key:
            api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("Anthropic API key must be provided or set in ANTHROPIC_API_KEY environment variable")
        self.client = Anthropic(api_key=api_key)
        self.model = model or self.DEFAULT_MODEL


    def generate_podcast_transcript(self, content):
        """Generate podcast transcript using Claude

        Args:
            content (str): Input content to generate podcast from

        Returns:
            str: Generated podcast transcript
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=GEN_POD_SYSTEM_PROMPT,
                messages=[{
                    "role": "user",
                    "content": content
                }]
            )
            return response.content[0].text

        except Exception as e:
            logging.error(f"Error generating transcript with Claude: {str(e)}")
            raise e