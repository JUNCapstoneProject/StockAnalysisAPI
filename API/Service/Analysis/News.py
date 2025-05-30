# Bridge
from Modules.AIAnalysis.Papers.FinReport.NewsFactorization import NewsFactorInput


class NewsAnalysisService:
    # TODO : 추후 다른 모델 제공 예정
    def __init__(self):
        self.news_input = NewsFactorInput(memoize=False)

    def sentiment_analysis(self, data):
        return self.news_input(data)
