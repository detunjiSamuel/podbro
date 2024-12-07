from content.base import ContentBase

import youtube_dl

"""
check link:
https://github.com/ytdl-org/youtube-dl/blob/master/README.md#how-can-i-detect-whether-a-given-url-is-supported-by-youtube-dl

"""


class Video(ContentBase):


    def is_valid_source(self):
        pass

    def download_video_from_url(self):
        # download the video using ytdl
        # return temp file path

        # might need to use ffmpeg to convert the video to a format that can be used by wispher

        # TODO : check if ydtcl can just auto download the audi
        pass

    def extract_audio_from_video(self):
        # extract audio from the video
        # return the audio file path
        pass

    def extract_content_from_source(self):
        # download the video with ytdl
        # extract the text from the video using wispher
        # return the text
        pass

