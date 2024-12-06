from unittest import TestCase
from parameterized import parameterized

from content.youtube import get_yt_video_id, YouTube

import os


class Test(TestCase):
    @parameterized.expand([
        ('https://youtu.be/Dlxu28sQfkE', 'Dlxu28sQfkE'),
        ('https://www.youtube.com/watch?v=Dlxu28sQfkE&feature=youtu.be', 'Dlxu28sQfkE'),
        ('https://www.youtube.com/watch/Dlxu28sQfkE', 'Dlxu28sQfkE'),
        ('https://www.youtube.com/embed/Dlxu28sQfkE', 'Dlxu28sQfkE'),
        ('https://www.youtube.com/v/Dlxu28sQfkE', 'Dlxu28sQfkE'),
    ])
    def test_get_yt_video_id(self, url, expected_video_id):
        self.assertEqual(expected_video_id, get_yt_video_id(url))


class TestYouTube(TestCase):

    def setUp(self):
        self.yt_transcript_path = os.path.join(os.path.dirname(__file__), 'data', 'sample_yt_transcript.txt')

    def test_extract_content_from_source(self):
        source = 'https://www.youtube.com/watch?v=ReiYJhgwrz4'
        yt = YouTube(source)
        transcript = yt.extract_content_from_source()

        with open(self.yt_transcript_path, "r") as file:
            expected_transcript = file.read()

        self.assertIsNotNone(transcript)

        self.assertEqual(expected_transcript[:500], transcript[:500])
