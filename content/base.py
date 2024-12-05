from abc import ABC, abstractmethod


class ContentBase(ABC):

    def __init__(self, source):
        self.source = source

        if not self.is_valid_source():
            raise Exception("Invalid source passed")

    @abstractmethod
    def is_valid_source(self):
        pass

    @abstractmethod
    def extract_content_from_source(self):
        pass
