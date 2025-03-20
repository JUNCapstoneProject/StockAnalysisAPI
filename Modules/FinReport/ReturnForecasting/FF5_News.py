from Modules.Azure.ml import EndPoints


class SentimentClassifier(EndPoints):
    ENDPOINTS_URL = "https://tokenizer-endpoint-3ff719b6.koreacentral.inference.ml.azure.com/score"

    @classmethod
    def _azureml(cls, news_data):
        data = {
            'data': news_data
        }
        cls.request(cls.ENDPOINTS_URL, data)
