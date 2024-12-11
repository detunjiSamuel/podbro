from abc import ABC, abstractmethod


class ContentBase(ABC):

    def __init__(self, source):
        self.source = source

        if not self.is_valid_source():
            raise Exception("Invalid source passed")

    def is_valid_source(self):
        return bool(self.__class__.validate_source(self.source))

    @staticmethod
    @abstractmethod
    def validate_source(source):
        """
        This method should be used to validate the source passed in
        it is static method so that it can be used to validate the source before creating the object
        :param source:
        :return:
        """
        pass

    @abstractmethod
    def extract_content_from_source(self):
        pass
