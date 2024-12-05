from content.base import ContentBase

from youtube_transcript_api import YouTubeTranscriptApi

import re

import logging


def regex_search(pattern: str, string: str, group: int) -> str:
    """Shortcut method to search a string for a given pattern.

    :param str pattern:
        A regular expression pattern.
    :param str string:
        A target string to search.
    :param int group:
        Index of group to return.
    :rtype:
        str or tuple
    :returns:
        Substring pattern matches.
    """
    regex = re.compile(pattern)
    results = regex.search(string)
    if not results:
        raise Exception("No match found for pattern: %s" % pattern)

    logging.debug("matched regex search: %s", pattern)

    return results.group(group)


def get_yt_video_id(url):
    """Extract the ``video_id`` from a YouTube url.

    This function supports the following patterns:

    - :samp:`https://youtube.com/watch?v={video_id}`
    - :samp:`https://youtube.com/embed/{video_id}`
    - :samp:`https://youtu.be/{video_id}`

    :param str url:
        A YouTube url containing a video id.
    :rtype: str
    :returns:
        YouTube video id.
    """
    return regex_search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url, group=1)


class YouTube(ContentBase):

    def is_valid_source(self):
        try:
            get_yt_video_id(self.source)
            return True
        except Exception as e:
            logging.error(e)
            return False

    def extract_content_from_source(self):
        """
        Extracts transcript from a YouTube video

        :param source:
        :return:
        """

        video_id = get_yt_video_id(self.source)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        return chr(12).join([t['text'] for t in transcript]).lower()
