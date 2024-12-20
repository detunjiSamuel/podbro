from unittest import TestCase

from podbro.content_parsers.webpage import WebPage

from parameterized import parameterized


class TestWebPage(TestCase):

    def setUp(self):
        self.article_page = "https://quantgirl.blog/advent-calendar-2024-day-3-galton-watson/"

    def test_extract_content_from_news_article_success(self):
        author_expected = "Quant Girl"
        title_expected = "Advent Calendar 2024 Day 3: Galton-Watson"
        webpage_content = WebPage(self.article_page).extract_content_from_news_article()

        self.assertIsNotNone(webpage_content)
        self.assertIsInstance(webpage_content, str)
        self.assertTrue(author_expected in webpage_content)
        self.assertTrue(title_expected in webpage_content)

        with open("./data/sample_article.txt", "r") as file:
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

    def test_extract_content_from_source(self):
        # TODO: Implement this test
        # not feeling creative enough to write this test
        self.fail()
