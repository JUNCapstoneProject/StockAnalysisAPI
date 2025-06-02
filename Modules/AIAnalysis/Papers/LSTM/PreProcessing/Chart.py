from sklearn.preprocessing import RobustScaler
import pandas as pd
import numpy as np


class ChartPreProcessing:
    @classmethod
    def process(cls, chart: pd.DataFrame) -> pd.DataFrame:
        if len(chart["timestamp"]) < 260:  # 최소 1년치 데이터 필요함
            raise ValueError('최소 1년치 이상(260개)의 데이터가 필요합니다')
        else:
            label = cls.create_label(chart['o'], chart['c'])
            pre_processed_data = cls.create_stock_data(chart, label)
            cls.scalar_normalize(pre_processed_data)
            return pre_processed_data

    @staticmethod
    def create_label(df_open: pd.Series, df_close: pd.Series, perc=[0.5, 0.5]):
        perc = [0.] + list(np.cumsum(perc))
        if isinstance(df_open, pd.Series):
            ratio = df_close / df_open - 1
            label = pd.qcut(ratio.rank(method='first'), perc, labels=False)
        else:  # DataFrame일 경우
            ratio = df_close.iloc[:, 1:] / df_open.iloc[:, 1:] - 1
            label = ratio.apply(lambda x: pd.qcut(x.rank(method='first'), perc, labels=False), axis=1)

        return label[1:]

    @staticmethod
    def create_stock_data(chart, label, m=240):
        st_data = pd.DataFrame([])
        st_data['Date'] = list(chart['timestamp'])
        daily_change = chart['c'] / chart['o'] - 1
        for k in range(m)[::-1]:
            st_data['IntraR ' + str(k)] = daily_change.shift(k)

        nextday_ret = (np.array(chart['o'][1:]) / np.array(chart['c'][:-1]) - 1)
        nextday_ret = pd.Series(list(nextday_ret) + [np.nan])
        for k in range(m)[::-1]:
            st_data['NextR ' + str(k)] = nextday_ret.shift(k)

        close_change = chart['c'].pct_change()
        for k in range(m)[::-1]:
            st_data['CloseR ' + str(k)] = close_change.shift(k)

        st_data['IntraR-future'] = daily_change.shift(-1)
        st_data['label'] = list(label) + [np.nan]
        st_data['Month'] = list(chart['timestamp'].dt.strftime('%Y-%m'))
        st_data = st_data.dropna()

        # trade_year = st_data['Month'].str[:4]
        st_data = st_data.drop(columns=['Month'])
        st_data.set_index('Date', inplace=True)
        return st_data

    @staticmethod
    def scalar_normalize(chart):
        scaler = RobustScaler()
        scaler.fit(chart.iloc[:, 1:-2])
        chart.iloc[:, 1:-2] = scaler.transform(chart.iloc[:, 1:-2])
