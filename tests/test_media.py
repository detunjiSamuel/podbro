from unittest import TestCase

from content_parsers.media import download_video_file, video_to_audio

import os


class Test(TestCase):

    def setUp(self):
        self.files_generated = []

    def tearDown(self):
        for audio in self.files_generated:
            if os.path.exists(audio):
                os.remove(audio)

    def test_download_video_file(self):
        url = "https://www.youtube.com/watch?v=I4dbALnlezA"
        download_video_file(url)
        self.assertTrue(os.path.exists(
            "Trump Named Time's Person of the Year & NJ Drones Incite Conspiracy Theories ｜ The Daily Show [I4dbALnlezA].webm"))

        self.files_generated.append(
            "Trump Named Time's Person of the Year & NJ Drones Incite Conspiracy Theories ｜ The Daily Show [I4dbALnlezA].webm")

    def test_video_to_audio(self):

        if not os.path.exists(
                "Trump Named Time's Person of the Year & NJ Drones Incite Conspiracy Theories ｜ The Daily Show [I4dbALnlezA].webm"):
            download_video_file("https://www.youtube.com/watch?v=I4dbALnlezA")

        file_name = "Trump Named Time's Person of the Year & NJ Drones Incite Conspiracy Theories ｜ The Daily Show [I4dbALnlezA].webm"

        video_file_path = os.path.join(os.path.dirname(__file__), file_name)

        result = video_to_audio(
            video_file_path,
        )

        base_name, _ = os.path.splitext(video_file_path)
        output_audio = f"{base_name}.mp3"

        self.assertTrue(os.path.exists(output_audio))

        self.files_generated.append(output_audio)
        self.files_generated.append(file_name)
