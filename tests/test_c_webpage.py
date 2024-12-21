from unittest import TestCase
from unittest.mock import patch, Mock

from podbro.content_parsers.webpage import WebPage

from parameterized import parameterized

import os


class TestWebPage(TestCase):

    def setUp(self):
        self.article_page = "https://quantgirl.blog/advent-calendar-2024-day-3-galton-watson/"
        self.web_page = "https://example.com"

    def test_extract_content_from_news_article_success(self):
        author_expected = "Quant Girl"
        title_expected = "Advent Calendar 2024 Day 3: Galton-Watson"
        webpage_content = WebPage(self.article_page).extract_content_from_news_article()

        self.assertIsNotNone(webpage_content)
        self.assertIsInstance(webpage_content, str)
        self.assertTrue(author_expected in webpage_content)
        self.assertTrue(title_expected in webpage_content)

        with open(
                os.path.join(os.path.dirname(__file__), 'data', 'sample_article.txt'),
                "r"
        ) as file:
            expected_content = file.read()
            self.assertEqual(expected_content[:500], webpage_content[:500])

    @parameterized.expand([
        "https://www.google.com/",
        "https://www.youtube.com/",
        "https://www.facebook.com/",
        "https:/github.com/",
        "https:/pinterest.com/"
    ])
    def test_extract_content_from_news_article_failure(self, url):
        with self.assertRaises(Exception):
            WebPage(url).extract_content_from_news_article()

    @patch('requests.get')
    def test_extract_content_from_webpage_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><p>Example content</p></body></html>"
        mock_get.return_value = mock_response

        webpage_content = WebPage(self.web_page).extract_content_from_webpage()

        self.assertIsNotNone(webpage_content)
        self.assertIsInstance(webpage_content, str)
        self.assertIn("Example content", webpage_content)

    @patch('requests.get')
    def test_extract_content_from_webpage_failure(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.assertRaises(Exception):
            WebPage(self.web_page).extract_content_from_webpage()

    @parameterized.expand([
        ("https://www.example.com", True),
        # The test below : Exposes a bug in the code
        ("ftp://example.com", False),
        ("http://", False),
        ("", False)
    ])
    def test_validate_source(self, url, expected):
        self.assertEqual(WebPage.validate_source(url), expected)

    @patch.object(WebPage, 'extract_content_from_news_article')
    @patch.object(WebPage, 'extract_content_from_webpage')
    def test_extract_content_from_source(self, mock_extract_webpage, mock_extract_article):
        mock_extract_article.side_effect = Exception("Article extraction failed")
        mock_extract_webpage.return_value = "Webpage content"

        webpage_content = WebPage(self.web_page).extract_content_from_source()

        self.assertIsNotNone(webpage_content)
        self.assertIsInstance(webpage_content, str)
        self.assertEqual(webpage_content, "Webpage content")

    @patch.object(WebPage, 'extract_content_from_news_article')
    @patch.object(WebPage, 'extract_content_from_webpage')
    def test_extract_content_from_source_all_fail(self, mock_extract_webpage, mock_extract_article):
        mock_extract_article.side_effect = Exception("Article extraction failed")
        mock_extract_webpage.side_effect = Exception("Webpage extraction failed")

        with self.assertRaises(Exception):
            WebPage(self.web_page).extract_content_from_source()