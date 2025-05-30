import numpy as np
import unittest

import pandas as pd

# LSTM
from Modules.AIAnalysis.Papers.LSTM.Adapter import adapter
from Modules.AIAnalysis.Papers.LSTM.PreProcessing.Chart import ChartPreProcessing as CPP
from Modules.AIAnalysis.Papers.LSTM.PreProcessing.Finance import FinancePreProcessing as FPP
from Modules.AIAnalysis.Papers.LSTM.PreProcessing.Merge import merge
from Modules.AIAnalysis.Papers.LSTM.Lstm import FinanceLSTM
from Modules.AIAnalysis.Papers.LSTM import FinanceInput
# TEST
from tests.DummyData.Finance.Chart import *
from Statistics import Statistics


def simulate(test_data: pd.DataFrame, predictions: np.ndarray):
    rets = pd.DataFrame([], columns=['Long', 'Short'])
    k = 10

    test_data = test_data.copy()
    test_data['pred'] = predictions

    for day in sorted(test_data['date'].unique()):
        daily_data = test_data[test_data['date'] == day]
        sorted_data = daily_data.sort_values('pred', ascending=False)

        long_returns = sorted_data['CloseR0'].iloc[:k]
        short_returns = -sorted_data['CloseR0'].iloc[-k:]

        rets.loc[day] = [long_returns.mean(), short_returns.mean()]

    print('Result :', rets.mean())
    return rets


class LstmTest(unittest.TestCase):
    pass
    # Success
    # def test_message(self):
    #     self.assertTrue(get_item())
    #     self.assertTrue(get_message())
    #     print('success test_message')

    # Success
    # def test_preprocess(self):
    #     test_message = get_message()
    #     item = test_message['body']['item']
    #     self.assertTrue(items)
    #     # 데이터 형식 변환
    #     data = test_adapter(item['data'])
    #     # 차트 데이터 전처리
    #     """
    #     # TODO : 이거 240일치 데이터는 안 되고 365일치는 일단 통과했다?
    #     # TODO : create_stock_data에서 st_data.dropna()가 empty 반환한거 아냐?
    #     """
    #     chart = CPP.process(data['chart'])
    #     self.assertFalse(chart.empty)  # 데이터프레임이 비어있으면 안 됨
    #     # 재무제표 데이터 전처리
    #     finance = FPP.process(data['balance_sheet'],
    #                           data['income_statement'],
    #                           data['cash_flow'])
    #     self.assertFalse(finance.empty)  # 데이터프레임이 비어있으면 안 됨
    #     # 데이터 가공합병
    #     merged_df = merge(finance, chart)
    #     self.assertFalse(merged_df.empty)  # 데이터프레임이 비어있으면 안 됨
    #
    #     print('success test_preprocess')

    # Success
    # def test_predict(self):
    #     test_message = get_message()
    #     item = test_message['body']['item']
    #     self.assertTrue(item)
    #     finance_input = FinanceInput(True)
    #     finance_output = finance_input(item['data'])
    #     pipeline_id = finance_output['pipeline_id']
    #     self.assertTrue(pipeline_id)
    #     prediction = finance_output['result']
    #     self.assertTrue(prediction)

    def test_performance(self):
        test_df = pd.read_csv('./DummyData/Finance/test.csv', index_col=0)
        # print(test_df.columns)
        input_df = test_df.drop(columns=['Unnamed: 0', 'Date'])  # , 'date'

        lstm = FinanceLSTM()
        predictions = lstm.prediction(input_df)
        returns = simulate(test_df, predictions)
        print('\nAverage returns prior to transaction charges')
        result_long = Statistics(returns['Long'])
        result_long.report()
        result_short = Statistics(returns['Short'])
        result_short.report()


if __name__ == "__main__":
    unittest.main()
