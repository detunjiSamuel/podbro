from openai import OpenAI
from enum import Enum

from abc import ABC, abstractmethod




class ModelProvider(str, Enum):
    """Supported model providers"""
    OPENAI = "openai"
    CLAUDE = "claude"
    LLAMA = "llama"


class GeneratorBase(ABC):
    """Abstract base class for all generator implementations"""

    @abstractmethod
    def generate_podcast_transcript(self, content):
        """Generate podcast transcript from content

        Args:
            content (str): Input content to generate podcast from

        Returns:
            str: Generated podcast transcript
        """
        pass


def get_generator(provider: ModelProvider, **kwargs):
    """Factory function to get appropriate generator implementation

    Args:
        provider (ModelProvider): The model provider to use
        **kwargs: Additional arguments passed to the generator constructor

    Returns:
        GeneratorBase: Instance of the appropriate generator class
    """
    if provider == ModelProvider.OPENAI:
        from podbro.generator.openai import OpenAIGenerator
        return OpenAIGenerator(**kwargs)
    elif provider == ModelProvider.CLAUDE:
        from podbro.generator.claude import ClaudeGenerator
        return ClaudeGenerator(**kwargs)
    elif provider == ModelProvider.LLAMA:
        from podbro.generator.llama import LlamaGenerator
        return LlamaGenerator(**kwargs)
    else:
        raise ValueError(f"Unsupported model provider: {provider}")


def generate_podcast_transcript(content, provider=ModelProvider.OPENAI, **kwargs):
    """Helper function to generate transcript using specified provider

    Args:
        content (str): Input content to generate from
        provider (ModelProvider): Model provider to use
        **kwargs: Additional arguments for the generator

    Returns:
        str: Generated podcast transcript
    """
    generator = get_generator(provider, **kwargs)
    return generator.generate_podcast_transcript(content)



def parse_transcript(content):
    """
    Parses a dialogue string and returns an array of tuples with speaker and their dialogue

    Assumes the dialogue is in the format:  Speaker: Dialogue

    :param content: str
    :return: [(speaker, dialogue)]
    """
    transcript_arr = []
    curr_speaker = None
    curr_text = ""

    for line in content.split("\n"):
        index = line.find(":")
        if index == -1:
            curr_text += line
        else:
            if curr_speaker:
                transcript_arr.append((curr_speaker, curr_text))
            curr_speaker = line[:index]
            curr_text = line[index + 1:]
    return transcript_arr
