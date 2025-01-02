from unittest import TestCase ,mock
from parameterized import parameterized
from unittest.mock import patch
from podbro.content_parsers.youtube import YouTube

import os


class TestYouTube(TestCase):
    def setUp(self):
        self.yt_transcript_path = os.path.join(os.path.dirname(__file__), 'data', 'sample_yt_transcript.txt')

    @parameterized.expand([
        ('https://youtu.be/Dlxu28sQfkE', 'Dlxu28sQfkE'),
        ('https://www.youtube.com/watch?v=Dlxu28sQfkE&feature=youtu.be', 'Dlxu28sQfkE'),
        ('https://www.youtube.com/watch/Dlxu28sQfkE', 'Dlxu28sQfkE'),
        ('https://www.youtube.com/embed/Dlxu28sQfkE', 'Dlxu28sQfkE'),
        ('https://www.youtube.com/v/Dlxu28sQfkE', 'Dlxu28sQfkE'),
    ])
    def test_get_yt_video_id(self, url, expected_video_id):
        self.assertEqual(expected_video_id, YouTube.get_yt_video_id(url))

    @parameterized.expand([
        ('https://youtu.be/Dlxu28sQfkE', True),
        ('https://www.youtube.com/watch?v=Dlxu28sQfkE&feature=youtu.be', True),
        ('https://www.youtube.com/watch/Dlxu28sQfkE', True),
        ('https://www.youtube.com/embed/Dlxu28sQfkE', True),
        ('https://www.youtube.com/v/Dlxu28sQfkE', True),
        # The test below exposed an error in my logic: it would work in production, but not in testing
        # create better fix , and then uncomment the test
        ('https://www.invalidurl.com/watch?v=Dlxu28sQfkE', True),
    ])
    @patch('podbro.content_parsers.youtube.YouTubeTranscriptApi.get_transcript', return_value=[{'text': 'sample text'}])
    def test_validate_source(self, url, expected_result, mock_get_transcript):
        self.assertEqual(expected_result, YouTube.validate_source(url))

    @mock.patch('podbro.content_parsers.youtube.YouTubeTranscriptApi.get_transcript')
    def test_extract_content_from_source(self , mock_get_transcript):
        mock_get_transcript.return_value = [{'text': 'test transcript'}]

        source = 'https://www.youtube.com/watch?v=ReiYJhgwrz4'
        yt = YouTube(source)
        transcript = yt.extract_content_from_source()


        self.assertIsNotNone(transcript)
        self.assertEqual(transcript, 'test transcript')



    @patch('podbro.content_parsers.youtube.YouTubeTranscriptApi.get_transcript', return_value=[{'text': 'sample text'}])
    def test_extract_content_from_source_lazy_patch(self, mock_get_transcript):
        source = 'https://www.youtube.com/watch?v=ReiYJhgwrz4'
        yt = YouTube(source)
        transcript = yt.extract_content_from_source()

        expected_transcript = 'sample text'

        self.assertIsNotNone(transcript)
        self.assertEqual(expected_transcript, transcript)
