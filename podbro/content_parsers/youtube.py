from podbro.content_parsers.base import ContentBase

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
    :raises Exception:
        If no match is found for the pattern.
    """
    regex = re.compile(pattern)
    results = regex.search(string)
    if not results:
        raise Exception("No match found for pattern: %s" % pattern)

    logging.debug("matched regex search: %s", pattern)
    return results.group(group)


class YouTube(ContentBase):
    """Class to handle YouTube content extraction."""

    @staticmethod
    def get_yt_video_id(url: str):
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
        :raises Exception:
            If no video id is found in the url.
        """
        return regex_search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url, group=1)

    @staticmethod
    def validate_source(source : str):
        """Validate the YouTube source.

         This method checks if the source is a valid YouTube URL and if the video has a transcript available.

         :param str source:
             The YouTube URL to validate.
         :rtype: bool
         :returns:
             True if the source is valid, False otherwise.
         """
        try:
            id = YouTube.get_yt_video_id(source)  # this will raise an exception if the source is invalid
            YouTubeTranscriptApi.get_transcript(id)
            # there are cases when a youtuber manually disables subtitle
            # might need better error way to check , i dont like the idea of calling the api to check
            # TODO : consider just passing control to main media if extraction fails at youtube level
            # this might make mroe sense
            return True
        except Exception as e:
            logging.error(e)
            return False

    def extract_content_from_source(self):
        """Extracts transcript from a YouTube video.

         :rtype: str
         :returns:
             The transcript of the YouTube video as a single string.
         :raises Exception:
             If the transcript cannot be retrieved.
         """

        video_id = self.__class__.get_yt_video_id(self.source)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return chr(12).join([t['text'] for t in transcript]).lower()
