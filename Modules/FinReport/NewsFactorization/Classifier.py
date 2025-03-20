from Interfaces.interface import FactorInterface
from Modules.Azure.ml import EndPoints


class SentimentClassifier(FactorInterface):
    API_KEY = '1Qzrzfw6xGP3wJUeVLqiDDHIyGgUsLQ9'
    ENDPOINTS_URL = ''

    @classmethod
    def create_factor(cls, datas):
        return EndPoints.request(cls.ENDPOINTS_URL, datas)
