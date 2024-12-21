import newspaper.article

from podbro.content_parsers.base import ContentBase

import requests
from newspaper import Article
from bs4 import BeautifulSoup

from urllib.parse import urlparse

import logging


def is_valid_url(url: str):
    """
    Validate if the given URL is properly formatted.

    :param url: The URL to validate.
    :return: True if the URL is valid, False otherwise.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


class WebPage(ContentBase):
    """
    Class to handle content extraction from web pages and news articles.
    """
    @staticmethod
    def validate_source(source: str):
        """
        Validate if the source is a valid URL.

        :param source: The source URL to validate.
        :return: True if the source is a valid URL, False otherwise.
        """
        return is_valid_url(source)

    def extract_content_from_news_article(self):
        """
        Extract content from a news article using the newspaper library.

        :return: The extracted content including author, title, and text.
        :raises: Exception if the article is invalid or an error occurs during extraction.
        """
        article = Article(url=self.source)
        try:
            article.download()
            article.parse()

            if not article.is_valid_body():
                # without this , pages like 'google.com' will pass
                raise newspaper.article.ArticleException("Invalid article body")
            return f"Author: {article.authors} \n\n Title: {article.title} \n\n {article.text}"
        except newspaper.article.ArticleException as e:
            logging.error(e)
            raise Exception(f"Error not an article passed into news article extractor : {self.source}")
        except Exception as e:
            logging.error(e)
            raise Exception(f"Error while extracting content_parsers from the article : {self.source}")

    def extract_content_from_webpage(self):
        """
        Extract content from a general web page using requests and BeautifulSoup.

        :return: The extracted text content from the web page.
        :raises: Exception if an error occurs during extraction.
        """
        try:
            response = requests.get(self.source)
            if response.status_code != 200:
                raise Exception(f"Error while extracting content_parsers from the webpage : {self.source}")
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.get_text()
        except Exception as e:
            logging.error(e)
            raise Exception(f"Error while extracting content_parsers from the webpage : {self.source}")

    def extract_content_from_source(self):
        """
        Extract content from the source URL. Tries to extract as a news article first, then as a general web page.

        :return: The extracted content.
        :raises: Exception if all extraction methods fail.
        """

        methods = [
            # the order of methods is important
            self.extract_content_from_news_article,
            self.extract_content_from_webpage
        ]
        last_exception = None

        for method in methods:
            try:
                result = method()
                return result
            except Exception as e:
                logging.error(e)
                last_exception = e

        # If all methods fail, raise an exception
        raise Exception("Another Extract content_parsers with available methods") from last_exception
