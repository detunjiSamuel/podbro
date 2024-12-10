from unittest import TestCase
from content_parsers.pdf import Pdf
import os


class TestPdf(TestCase):
    def setUp(self):
        self.max_content_length = 50000
        self.pdf_path = os.path.join(os.path.dirname(__file__), 'data', 'sample.pdf')
        self.expected_path = os.path.join(os.path.dirname(__file__), 'data', 'sample.txt')

        self.pdf_content = Pdf(self.pdf_path)

    def test_extract_text_from_pdf(self):
        content = self.pdf_content.extract_content_from_source(self.max_content_length)

        self.assertIsNotNone(content)
        self.assertIsInstance(content, str)

        with open(self.expected_path, "r") as file:
            self.assertEqual(content[:self.max_content_length], file.read()[:self.max_content_length])
