import logging
import os

import pymupdf

from content_parsers.base import ContentBase


def file_exists(file_path):
    if not os.path.exists(file_path):
        logging.error("Invalid FILE PATH")
        return False
    return True


class Pdf(ContentBase):

    @staticmethod
    def validate_source(pdf_path):
        if not file_exists(pdf_path):
            logging.error("Invalid PDF PATH")
            return False
        if not pdf_path.endswith('.pdf'):
            logging.error("Invalid FILE TYPE")
            return False
        return True

    def extract_content_from_source(self, MAX_CHAR_LENGTH=None):
        pdf_path = self.source
        with pymupdf.open(pdf_path) as doc:
            pdf_content = []
            total_chars = 0
            for page in doc:
                text = page.get_text()
                if MAX_CHAR_LENGTH and total_chars + len(text) > MAX_CHAR_LENGTH:
                    pdf_content.append(
                        page.get_text()[:MAX_CHAR_LENGTH - total_chars])
                    break
                pdf_content.append(text)
                total_chars += len(text)
        return chr(12).join(pdf_content)
