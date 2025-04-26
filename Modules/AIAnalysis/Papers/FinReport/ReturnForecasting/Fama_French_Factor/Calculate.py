import yfinance as yf
import pandas as pd
import numpy as np
# bridge
from Modules.AIAnalysis.Papers.FinReport.ReturnForecasting.Fama_French_Factor.Get import GetFinanceIndex as Get
from Modules.AIAnalysis.Papers.FinReport.ReturnForecasting.Fama_French_Factor.Classifiy import ClassifiyCompanies as Classifiy


class CalculateFactor:
    @staticmethod
    def roe(ticker):
        """
        주어진 기업의 ROE (Return on Equity)를 계산하는 함수입니다.
        :param ticker: 기업 티커
        :param stock_data: 각 기업의 주식 데이터
        :return: 해당 기업의 ROE 값
        """
        stock = yf.Ticker(ticker)
        financials = stock.financials  # 손익계산서

        # 날짜별로 필요한 컬럼(순이익 및 총수익) 추출
        normalized_income = financials.loc['Normalized Income']
        total_revenue = financials.loc['Total Revenue']

        # ROE 계산: 순이익 / 총수익
        roe = normalized_income / total_revenue
        return roe

    @staticmethod
    def rmt_factor(market_data):
        rmt_factor = market_data['Adj Close'].pct_change().dropna()
        rmt_factor.name = 'Market'
        return rmt_factor

    @staticmethod
    def cma_factor(stock_data, quantile_ratio=0.3):
        """
        CMA (Conservative Minus Aggressive) 요인을 날짜별로 계산합니다.
        :param stock_data: 각 기업의 주식 데이터 (주식 수익률)
        :param capex_data: 각 기업의 CapEx 데이터
        :param quantile_ratio: 하위 30%를 기준으로 분할할 비율
        :return: 날짜별 CMA 요인
        """
        tickers = stock_data.columns.get_level_values(1).unique().tolist()
        capex_data = Get.capex_data(tickers)
        aggressive, conservative = ClassifiyCompanies.by_capex(capex_data, quantile_ratio)

        cma_factors = []

        # 각 날짜별로 CMA 계산
        for date in stock_data.index:
            # 해당 날짜에 대한 수익률을 구하기
            aggressive_return = stock_data.loc[date].iloc[aggressive.index].mean()
            conservative_return = stock_data.loc[date].iloc[conservative.index].mean()

            # CMA 계산
            cma_factor = conservative_return - aggressive_return
            cma_factors.append(cma_factor)

        # 날짜별 CMA 요인을 Series로 반환
        cma_series = pd.Series(cma_factors, index=stock_data.index.strftime('%Y-%m-%d'), name='CMA')
        return cma_series

    @staticmethod
    def smb_factor(stock_data):
        smb_values = []
        for date, daily_data in stock_data.groupby('Date'):
            # Ticker별로 Market Cap을 가져오기
            market_caps = daily_data.xs('Market Cap', level=0, axis=1)

            # 소형주와 대형주의 구분
            small_cap_tickers = market_caps.columns[market_caps.iloc[0] < market_caps.quantile(0.3, axis=1).iloc[0]]
            big_cap_tickers = market_caps.columns[market_caps.iloc[0] > market_caps.quantile(0.7, axis=1).iloc[0]]

            # 소형주와 대형주의 Adj Close 추출
            small_cap = daily_data.xs('Adj Close', level=0, axis=1)[small_cap_tickers]
            big_cap = daily_data.xs('Adj Close', level=0, axis=1)[big_cap_tickers]

            # SMB 계산: 소형주와 대형주의 수익률 차이
            smb_value = small_cap.mean(axis=1).mean() - big_cap.mean(axis=1).mean()
            smb_values.append(smb_value)

        smb_factor = pd.Series(smb_values, index=stock_data.groupby('Date').first().index.strftime('%Y-%m-%d'), name='SMB')
        return smb_factor

    @staticmethod
    def hml_factor(stock_data):
        """
        HML (High Minus Low) 요인을 날짜별로 계산합니다.
        :param stock_data: 각 기업의 주식 데이터 (주식 수익률)
        :param high_pb: P/B 비율 상위 30% 기업 리스트
        :param low_pb: P/B 비율 하위 30% 기업 리스트
        :return: 날짜별 HML 요인
        """
        tickers = stock_data.columns.get_level_values(1).unique().tolist()
        pb_data = Get.pb_ratio(tickers)
        high_pb, low_pb = Classifiy.by_pb(pb_data)

        # 실제 존재하는 주식들만 필터링
        valid_high_pb = [ticker for ticker in high_pb
                         if ticker in stock_data.columns.get_level_values(1)]
        valid_low_pb = [ticker for ticker in low_pb
                        if ticker in stock_data.columns.get_level_values(1)]

        # 날짜별 수익률 계산
        returns = stock_data.pct_change()
        returns.fillna(0, inplace=True)

        # 각 날짜에 대해 HML 요인 계산
        hml_factors = []
        for date, daily_data in returns.groupby('Date'):
            # High(상위)와 Low(하위) 포트폴리오 수익률 계산
            daily_data_adj_close = daily_data.xs('Adj Close', level=0, axis=1)
            high_pb_returns = daily_data_adj_close[valid_high_pb].mean().mean()  # 상위 기업 평균 수익률
            low_pb_returns = daily_data_adj_close[valid_low_pb].mean().mean()  # 하위 기업 평균 수익률

            # HML 요인 계산 (High Minus Low)
            hml_factor = high_pb_returns - low_pb_returns
            hml_factors.append(hml_factor)

        # 날짜별로 HML 요인을 Series로 반환
        hml_factor_series = pd.Series(hml_factors, index=returns.groupby('Date').first().index.strftime('%Y-%m-%d'), name='HML')
        return hml_factor_series

    @classmethod
    def rmw_factor(cls, stock_data):
        """
        RMW (Robust Minus Weak) 요인을 날짜별로 계산합니다.
        :param stock_data: 각 기업의 주식 데이터 (주식 수익률)
        :return: 날짜별 RMW 요인
        """
        roe_values = pd.DataFrame(
            {ticker: cls.roe(ticker) for ticker in stock_data.columns.get_level_values(1)}
        ).ffill(axis=0).fillna(0)
        roe_values.index = pd.to_datetime(roe_values.index)

        # 각 날짜마다 ROE 상위 50%와 하위 50%를 구하여 RMW 계산
        rmw_factors = []
        for date in roe_values.index:
            # 해당 날짜의 ROE 값들만 추출
            date_roe = roe_values.loc[date].dropna()

            if len(date_roe) > 0:
                median_roe = np.median(date_roe)
                robust_roe = date_roe[date_roe > median_roe]  # 상위 50%
                weak_roe = date_roe[date_roe < median_roe]  # 하위 50%

                # 해당 날짜의 RMW 계산
                rmw_factor = robust_roe.mean() - weak_roe.mean()
                if np.isnan(rmw_factor):
                    rmw_factor = 0  # ROE가 없으면 0으로 처리
            else:
                rmw_factor = 0  # ROE가 없으면 0으로 처리

            rmw_factors.append(rmw_factor)

        # 날짜별로 RMW 요인을 Series로 반환
        rmw_factor_series = pd.Series(rmw_factors,
                                      index=roe_values.index.strftime('%Y-%m-%d'),
                                      name='RMW')
        return rmw_factor_series
