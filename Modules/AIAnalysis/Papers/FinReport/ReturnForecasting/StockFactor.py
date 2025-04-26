import pandas as pd
# bridge
from Modules.AIAnalysis.Papers.FinReport.ReturnForecasting.Fama_French_Factor.Calculate import CalculateFactor as Calculate


class QuantitativeFactor:
    @staticmethod
    def create_factor(stock_data, market_data):
        # 1. Market (S&P 500 등 전체 시장 수익률)
        rmt = Calculate.rmt_factor(market_data)
        # 2. SMB (Small Minus Big): 시가총액에 따른 두 포트폴리오의 수익률 차이
        smb = Calculate.smb_factor(stock_data)
        # 3. HML (High Minus Low): P/B 비율에 따른 두 포트폴리오의 수익률 차이
        hml = Calculate.hml_factor(stock_data)
        # 4. RMW (Robust Minus Weak): ROE에 따른 두 포트폴리오의 수익률 차이
        rmw = Calculate.rmw_factor(stock_data)
        # 5. CMA
        cma = Calculate.cma_factor(stock_data)

        ff5_factors = pd.concat([rmt, smb, hml, rmw, cma], axis=1)
        ff5_factors.info()
        if not isinstance(ff5_factors.index, pd.DatetimeIndex):
            ff5_factors.index = pd.to_datetime(ff5_factors.index, errors='coerce')

        ff5_factors.index = ff5_factors.index.strftime('%Y-%m-%d')
        ff5_factors = ff5_factors.ffill(axis=0).fillna(0)
        return ff5_factors
