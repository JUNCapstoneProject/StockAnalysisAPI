# Bridge
from Modules.Utils.Interfaces.Pipeline import Output
from Modules.AIAnalysis.Papers.LSTM import FinanceInput


class FinanceAnalysisService:
    # TODO : 추후 다른 모델 제공 예정
    def __init__(self):
        self.finance_input = FinanceInput(is_call=True)

    def lstm_analysis(self, data) -> Output:
        finance_output = self.finance_input(data)
        return finance_output
