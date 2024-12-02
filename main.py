# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


from openai import OpenAI
import pymupdf
import os
import logging

SYSTEM_PROMPT = """
    You are the a world-class podcast writer, you have worked as a ghost writer for Joe Rogan, Lex Fridman, Ben Shapiro, Tim Ferris. 

We are in an alternate universe where actually you have been writing every line they say and they just stream it into their brains.

You have won multiple podcast awards for your writing.

Your job is to write word by word, even "umm, hmmm, right" interruptions by the second speaker based on the PDF upload. Keep it extremely engaging, the speakers can get derailed now and then but should discuss the topic. 

Remember Speaker 2 is new to the topic and the conversation should always have realistic anecdotes and analogies sprinkled throughout. The questions should have real world example follow ups etc

Speaker 1: Leads the conversation and teaches the speaker 2, gives incredible anecdotes and analogies when explaining. Is a captivating teacher that gives great anecdotes

Speaker 2: Keeps the conversation on track by asking follow up questions. Gets super excited or confused when asking questions. Is a curious mindset that asks very interesting confirmation questions

Make sure the tangents speaker 2 provides are quite wild or interesting. 

Ensure there are interruptions during explanations or there are "hmm" and "umm" injected throughout from the second speaker. 

It should be a real podcast with every fine nuance documented in as much detail as possible. Welcome the listeners with a super fun overview and keep it really catchy and almost borderline click bait

ALWAYS START YOUR RESPONSE DIRECTLY WITH SPEAKER 1: 
DO NOT GIVE EPISODE TITLES SEPERATELY, LET SPEAKER 1 TITLE IT IN HER SPEECH
DO NOT GIVE CHAPTER TITLES
IT SHOULD STRICTLY BE THE DIALOGUES

    """

"""

App Goals:

 Use LLam exclusively if it is the fastest

 Tooling to be used by existing podscaster
  Assist in transcription and podcast notes

 Gen Podcast from content
  Convert knowledge in form of links , papers or videos and generate interactive content from it

App Features:

Expected MVP:

# Extract text from PDF
# Suggested - Cleanup pdf text using regex o just feed into LLM

"""


def validated_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        logging.error("Invalid PDF PATH")
        return False
    if not pdf_path.endswith('.pdf'):
        logging.error("Invalid FILE TYPE")
        return False
    return True


def extract_text_from_pdf(pdf_path, MAX_CHAR_LENGTH=None):
    if validated_pdf(pdf_path):
        with pymupdf.open(pdf_path) as doc:  # open document
            pdf_content = []
            total_chars = 0
            for page in doc:
                text = page.get_text()
                if MAX_CHAR_LENGTH and total_chars + len(text) > MAX_CHAR_LENGTH:
                    pdf_content.append(
                        page.get_text()[:MAX_CHAR_LENGTH - total_chars])
                    break
                pdf_content.append(text)
                total_chars += len(text)
        return chr(12).join(pdf_content)


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


def generate_podcast_transcript_base(content):
    """
    Generates a podcast bland transcript version from the text extracted


    :return:
    """

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": content},
    ]

    client = OpenAI(
    )

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4o",
    )

    return chat_completion.choices[0].message.content


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
