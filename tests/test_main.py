import os
from unittest import TestCase

from podbro.main import PodcastGenerator, ContentParser, TTSModel

import logging

logging.basicConfig(level=logging.INFO)


class TestContentParser(TestCase):

    def test_validate_sources_with_invalid_url(self):
        invalid_url = "utube.com/watch?v=VzJG4IpYDvs"

        with self.assertRaises(ValueError) as context:
            ContentParser.validate_sources([invalid_url], [])

        self.assertTrue("Invalid URL" in str(context.exception))

    def test_validate_sources_with_invalid_file(self):
        invalid_file = "/data/doesnotexist.mp3"

        with self.assertRaises(ValueError) as context:
            ContentParser.validate_sources([], [invalid_file])

        self.assertTrue("Invalid file path" in str(context.exception))

    def test_get_parser_mapping_caching(self):
        result1 = ContentParser.get_parser_mapping()
        result2 = ContentParser.get_parser_mapping()
        # should be same since i used caching
        self.assertIs(result1, result2)


class TestPodcastGenerator(TestCase):

    def setUp(self):
        self.generator = PodcastGenerator()
        self.valid_youtube_url = "https://www.youtube.com/watch?v=2CujHq4fb04"

    def test_extract_content_success(self):
        urls = [self.valid_youtube_url]
        files = []
        text = ""

        result = self.generator.extract_content(urls, files, text)
        # print( result )

        self.assertIsNotNone(result)
        self.assertTrue(len(result) > 0)

    def test_extract_content_failure(self):
        invalid_url = "utube.com/watch?v=VzJG4IpYDvs"
        invalid_file = "/data/doesnotexist.mp3"

        with self.assertRaises(Exception) as context:
            self.generator.extract_content([invalid_url], [], None)

        self.assertTrue("Invalid" in str(context.exception))

        with self.assertRaises(Exception) as context:
            self.generator.extract_content([], [invalid_file], None)

        self.assertTrue("Invalid" in str(context.exception))

    def test_create_podcast_success(self):
        urls = [self.valid_youtube_url]
        result = self.generator.create_podcast(
            urls=urls,
            files=[],
            text="",
            content_model="openai",
            tts_model=TTSModel.EDGE
        )
        print(result)
        self.assertTrue(os.path.exists(result))
        if os.path.exists(result):
            os.remove(result)

    def test_get_tts_model_caching(self):
        model1 = self.generator.get_tts_model(TTSModel.EDGE)
        model2 = self.generator.get_tts_model(TTSModel.EDGE)
        # should be same since i used cahcing
        self.assertIs(model1, model2)

    def test_get_tts_model_invalid(self):
        with self.assertRaises(ValueError) as context:
            self.generator.get_tts_model("invalid_model")
        self.assertTrue("Unsupported TTS model" in str(context.exception))
