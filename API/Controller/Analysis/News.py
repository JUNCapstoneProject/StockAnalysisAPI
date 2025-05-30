# Bridge
from API.Socket.Web.Decorator import *
from Modules.Utils.Interfaces.Pipeline import Output
from API.Utils.Error.Check import data_check
from API.Service.Analysis.News import NewsAnalysisService
from Utils.Error.UserError import UserInputError


@RequestMapping('/news')
class NewsAnalysisController:
    def __init__(self):
        self.news_service = NewsAnalysisService()

    @GetMapping('/sentiment_classifier')
    def sentiment_analysis(self, data) -> Output:
        try:
            data_check('/news/sentiment_classifier', data)
        except UserInputError as e:
            return Output(
                pipeline_id='None',
                return_time=None,
                status_code=e.status_code,
                message=str(e),
                data=None
            )
        else:
            output = self.news_service.sentiment_analysis(data)
            return output
