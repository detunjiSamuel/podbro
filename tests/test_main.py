from unittest import TestCase

from main import speech_to_text, extract_content
from podbro.content_parsers.media import break_audio_file_into_usable_chunks, download_file

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
        result = download_file(url2)
        self.fail()

    def test_extract_content(self):
        urls = [
            "https://www.youtube.com/watch?v=db0WO6BO5xo"
        ]

        files = [

        ]

        text = ""

        result = extract_content(urls, files, text)

        with open("modo_energy.txt", "w") as file:
            file.write(result)

        print(result)

        self.fail()  # fail it to draw attention to the test

    def test_extract_content_failure(self):
        # It is enough to test the failure
        # content parsers have their tests

        invalid_url = "utube.com/watch?v=VzJG4IpYDvs"
        invalid_file = "/data/doesnotexist.mp3"

        with self.assertRaises(Exception) as context:
            extract_content([invalid_url], [], None)

        self.assertTrue("Invalid URL" in str(context.exception))

        with self.assertRaises(Exception) as context:
            extract_content([], [invalid_file], None)

        self.assertTrue("Invalid FILE PATH" in str(context.exception))
