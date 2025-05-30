# Bridge
from API.Socket.Web.Decorator import *
from Modules.Utils.Interfaces.Pipeline import Output
from API.Utils.Error.Check import data_check
from API.Service.Analysis.Finance import FinanceAnalysisService
from Utils.Error.UserError import UserInputError


@RequestMapping('/finance')
class FinanceAnalysisController:
    def __init__(self):
        self.finance_service = FinanceAnalysisService()

    @GetMapping('/lstm')
    def lstm_analysis(self, data) -> Output:
        try:
            data_check('/finance/lstm', data)
        except UserInputError as e:
            return Output(
                pipeline_id='None',
                return_time=None,
                status_code=e.status_code,
                message=str(e),
                data=None
            )
        else:
            finance_output = self.finance_service.lstm_analysis(data)
            return finance_output
