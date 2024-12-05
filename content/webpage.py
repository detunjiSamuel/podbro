import newspaper.article

from content.base import ContentBase

import requests
from newspaper import Article
from bs4 import BeautifulSoup

from urllib.parse import urlparse

import logging


def is_valid_url(self):
    try:
        result = urlparse(self.url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


class WebPage(ContentBase):

    def is_valid_source(self):
        return is_valid_url(self.source)

    def extract_content_from_news_article(self):

        article = Article(url=self.source)
        try:
            article.download()
            article.download()
            return f"Author: {article.authors} \n\n Title {article.title} \n\n {article.text}"
        except newspaper.article.ArticleException as e:
            logging.error(e)
            raise Exception(f"Error not an article passed into news article extractor : {self.source}")
        except Exception as e:
            logging.error(e)
            raise Exception(f"Error while extracting content from the article : {self.source}")

    def extract_content_from_webpage(self):

        """
        Call get requests on url
        throw error is status code is not 200
        extract content from the webpage

        :return:
        """
        try:
            response = requests.get(self.source)
            if response.status_code != 200:
                raise Exception(f"Error while extracting content from the webpage : {self.source}")
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.get_text(separator="\n")
        except Exception as e:
            logging.error(e)
            raise Exception(f"Error while extracting content from the webpage : {self.source}")

    def extract_content_from_source(self):

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
        raise Exception("Another Extract content with available methods") from last_exception
