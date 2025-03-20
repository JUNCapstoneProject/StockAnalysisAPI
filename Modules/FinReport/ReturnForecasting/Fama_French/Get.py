import yfinance as yf
import pandas as pd
import numpy as np


class GetFinanceIndex:
    @staticmethod
    def pb_ratio(tickers):
        """
        각 기업의 P/B 비율을 가져옵니다.
        :param tickers: 주식 티커 리스트
        """
        pb_data = {}
        for ticker in tickers:
            try:
                # 각 기업의 재무 데이터를 가져오기 (P/B 비율)
                stock = yf.Ticker(ticker)
                # P/B 비율 (Price/Book)
                pb_ratio = stock.info['priceToBook']
                pb_data[ticker] = pb_ratio
            except Exception as e:
                print(f"Failed to get P/B ratio for {ticker}: {e}")
                pb_data[ticker] = np.nan
        return pd.Series(pb_data)

    @staticmethod
    def capex_data(tickers) -> pd.Series:
        """
        각 기업의 자본 지출(CapEx) 데이터를 가져옵니다.
        :param tickers: 주식 티커 리스트
        """
        capex_data = {}
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                financials = stock.financials  # 재무 데이터 가져오기

                # 'Reconciled Depreciation' 또는 다른 CapEx 관련 항목을 찾기
                capex = financials.loc['Reconciled Depreciation'] if 'Reconciled Depreciation' in financials.index else None
                capex_data[ticker] = capex
            except Exception as e:
                print(f"Failed to get CapEx for {ticker}: {e}")
                capex_data[ticker] = None

        return pd.Series(capex_data)
