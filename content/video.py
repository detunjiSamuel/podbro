from content.base import ContentBase

import youtube_dl

"""
check link:
https://github.com/ytdl-org/youtube-dl/blob/master/README.md#how-can-i-detect-whether-a-given-url-is-supported-by-youtube-dl

"""


class Video(ContentBase):

    def is_valid_source(self):
        pass

    def extract_content_from_source(self):
        # download the video with ytdl
        # extract the text from the video using wispher
        # return the text
        pass

