from unittest import TestCase
from podbro.content_parsers.pdf import Pdf
import os


class TestPdf(TestCase):
    def setUp(self):
        self.max_content_length = 50000
        self.pdf_path = os.path.join(os.path.dirname(__file__), 'data', 'sample.pdf')
        self.expected_path = os.path.join(os.path.dirname(__file__), 'data', 'sample.txt')

        self.invalid_pdf_path = os.path.join(os.path.dirname(__file__), 'data', 'invalid.pdf')
        self.pdf_content = Pdf(self.pdf_path)

    def test_extract_text_from_pdf(self):
        content = self.pdf_content.extract_content_from_source(self.max_content_length)

        self.assertIsNotNone(content)
        self.assertIsInstance(content, str)

        with open(self.expected_path, "r") as file:
            self.assertEqual(content[:self.max_content_length], file.read()[:self.max_content_length])

    def test_pdf_source_validation(self):
        does_not_exist = os.path.join(os.path.dirname(__file__), 'data', 'fake.pdf')
        not_a_pdf = os.path.join(os.path.dirname(__file__), 'data', 'sample.txt')

        self.assertFalse(Pdf.validate_source(does_not_exist))
        self.assertFalse(Pdf.validate_source(not_a_pdf))

    def test_extract_text_with_max_char_length(self):
        content = self.pdf_content.extract_content_from_source(100)

        self.assertIsNotNone(content)
        self.assertIsInstance(content, str)
        self.assertLessEqual(len(content), 100)

    def test_extract_text_from_invalid_pdf(self):
        with self.assertRaises(Exception):
            Pdf(self.invalid_pdf_path)
