from openai import OpenAI

from prompts.base import GEN_POD_SYSTEM_PROMPT


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


def generate_podcast_transcript(content):
    """
    Generates a podcast bland transcript version from the text extracted


    :return:
    """

    messages = [
        {"role": "system", "content_parsers": GEN_POD_SYSTEM_PROMPT},
        {"role": "user", "content_parsers": content},
    ]

    client = OpenAI(
    )

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4o",
    )

    return chat_completion.choices[0].message.content
