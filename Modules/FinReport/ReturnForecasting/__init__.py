# bridge
from Interfaces.interface import InputInterface
# NewsFactorization
from Modules.FinReport.NewsFactorization.Tokenizer import NewsTokenizer
from Modules.FinReport.NewsFactorization.SRL import TokenSRL
from Modules.FinReport.NewsFactorization.IntrinsicFactor import CalculateIndex as StockIndex
from Modules.FinReport.NewsFactorization.Classifier import SentimentClassifier
# ReturnForecasting
# from Modules.FinReport.ReturnForecasting.Fama_French
# from Modules.FinReport.ReturnForecasting.FF5_News import


class Input(InputInterface):
    def __init__(self, data):
        self.data = data

    def __call__(self, is_call):
        if is_call:
            return Output()
        else:
            # 메모이자이징
            return Output()


class Output:
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        pass
