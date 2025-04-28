# Bridge
from Modules.Utils.Socket.Web.Decorator import *
from API.Service.Analysis.News import NewsAnalysisService


@RequestMapping('/news')
class NewsAnalysisController:
    def __init__(self):
        self.news_service = NewsAnalysisService()

    @GetMapping('/sentiment_classifier')
    def sentiment_analysis(self, data):
        output = self.news_service.sentiment_analysis(data)
        return output
