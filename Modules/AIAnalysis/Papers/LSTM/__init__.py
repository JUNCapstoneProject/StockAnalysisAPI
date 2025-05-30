# bridge
from Modules.Utils.Interfaces.Pipeline import Input
from Modules.Utils.Decorator import memoization
# LSTM
from Modules.AIAnalysis.Papers.LSTM.Adapter import adapter
from Modules.AIAnalysis.Papers.LSTM.PreProcessing.Chart import ChartPreProcessing as CPP
from Modules.AIAnalysis.Papers.LSTM.PreProcessing.Finance import FinancePreProcessing as FPP
from Modules.AIAnalysis.Papers.LSTM.PreProcessing.Merge import merge
from Modules.AIAnalysis.Papers.LSTM.Lstm import FinanceLSTM


class FinanceInput(Input):
    MODEL_NUM = 2

    def __init__(self, is_call):
        """
        is_call은 해당 모델의 AI를 사용할건지 여부
        memoize는 해당 모델이 과거에 학습한 데이터를 가져올건지 여부
        따라서 memoize != is_call 관계가 성립함
        """
        self.memoize = not is_call
        self.module_name = 'finance'  # memoization 데코레이터가 사용하는 값

    @memoization
    @adapter
    def __call__(self, data):
        """
        입력에 json 객체를 넣으면 adapter 데코레이터가 올바른 형식으로 변환
        실제 반환은 memoization 데코레이터가 Output 객체를 반환함
        """
        if self.memoize:
            return  # @memoization에서 값을 채워넣음
        else:
            # 전처리
            chart = CPP.process(data['chart'])
            finance = FPP.process(data['balance_sheet'],
                                  data['income_statement'],
                                  data['cash_flow'])
            merged_df = merge(finance, chart)
            # 예측
            lstm = FinanceLSTM()
            prediction_class = lstm.prediction(merged_df)
            return prediction_class
