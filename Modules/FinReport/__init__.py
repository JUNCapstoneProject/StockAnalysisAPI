# bridge
from Interfaces.interface import InputInterface
# NewsFactorization
from Modules.FinReport.NewsFactorization import Input as NewsFactorization
# ReturnForecasting
# from Modules.FinReport.ReturnForecasting.Fama_French
# from Modules.FinReport.ReturnForecasting.FF5_News import


class Input(InputInterface):
    def __init__(self, data):
        self.data = data

    def __call__(self, is_call):
        if is_call:
            sentiment_factor = NewsFactorization(self.data)
            return Output()
        else:
            # 메모이자이징
            return Output()


class Output:
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        pass
