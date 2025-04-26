# bridge
from Modules.Utils.Interfaces.Pipeline import Input
from Modules.Utils.Decorator import memoization
from Modules.AIAnalysis.Papers.FinReport.Adapter import adapter
# NewsFactorization
from Modules.AIAnalysis.Papers.FinReport.NewsFactorization import NewsFactorInput
# ReturnForecasting
# from Modules.FinReport.ReturnForecasting.Fama_French_Factor
# from Modules.FinReport.ReturnForecasting.FF5_News import
from Modules.AIAnalysis.Papers.FinReport.ReturnForecasting import ForecastingInput


class FinReportInput(Input):
    MODEL_NUM = 1

    def __init__(self, is_call):
        """
        is_call은 해당 모델의 AI를 사용할건지 여부
        memoize는 해당 모델이 과거에 학습한 데이터를 가져올건지 여부
        따라서 memoize != is_call 관계가 성립함
        """
        self.memoize = not is_call

    def __call__(self, data):
        """
        실제 반환은 memoization 데코레이터가 처리
        Output 객체를 반환함
        """
        news_input = NewsFactorInput(self.memoize)
        news_output = news_input(data)
        sentiment_factor = news_output['result']
        return sentiment_factor
        # TODO : 추후 RiskAssessment 모듈 추가
        # forecast_input = ForecastingInput()
        # forecast_output = forecast_input(data)
        # return forecast_output['data']
