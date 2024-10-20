from abc import ABC, abstractmethod


class DataPreprocessor(ABC):
    """Data preprocessor class"""

    @abstractmethod
    def preprocess(self, data):
        pass


class OutlierRemover(DataPreprocessor):
    """Outlier removal algorithm"""

    def preprocess(self, data):
        return list(filter(lambda x: x < 10, data))


class Normalizer(DataPreprocessor):
    """Normalizer for data"""

    def preprocess(self, data):
        return list(map(lambda x: x / 10, data))


class Encoder(DataPreprocessor):
    """Encoder class for encoding data"""

    def __init__(self, encoding_dict=None):
        self.encoding_dict = encoding_dict or {}

    def preprocess(self, data):
        if data is None:
            return []

        return [self.encoding_dict.get(value, value) for value in data]
