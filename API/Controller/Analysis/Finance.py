# Bridge
from Modules.Utils.Socket.Web.Decorator import *
from Modules.Utils.Interfaces.Pipeline import Output
from API.Service.Analysis.Finance import FinanceAnalysisService


@RequestMapping('/finance')
class FinanceAnalysisController:
    def __init__(self):
        self.finance_service = FinanceAnalysisService()

    @GetMapping('/lstm')
    def lstm_analysis(self, data) -> Output:
        finance_output = self.finance_service.lstm_analysis(data)
        return finance_output
