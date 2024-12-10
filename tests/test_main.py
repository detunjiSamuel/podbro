from unittest import TestCase

from main import speech_to_text
from content_parsers.media import break_audio_file_into_usable_chunks, download_audio_file , download_video_file

import logging

logging.basicConfig(level=logging.INFO)


class Test(TestCase):
    def test_speech_to_text(self):
        result = speech_to_text()
        print(result)
        self.fail()

    def test_break_audio_file_into_usable_chunks(self):
        path = "/Users/bob/Documents/test/podbro/tests/We Rented BOYFRIENDS In Japan! [VzJG4IpYDvs].mp3"
        result = break_audio_file_into_usable_chunks(path)

        print(result)

        self.fail()

    def test_download_audio_file(self):
        url = "https://www.youtube.com/watch?v=VzJG4IpYDvs"
        url2 = "https://www.camdemy.com/media/14144"
        result = download_audio_file(url2)
        print(result)
        self.fail()