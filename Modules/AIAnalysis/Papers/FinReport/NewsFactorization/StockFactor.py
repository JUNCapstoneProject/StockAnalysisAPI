from sklearn.linear_model import LinearRegression
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import numpy as np
# bridge
from Utils.Error.UserError import UserInputError


class IntrinsicFactor:
    @classmethod
    def create_factor(cls, stock_history, market_history) -> list:
        return [
            cls._bias(stock_history).iloc[-1],
            cls._vmacd(stock_history)[0].iloc[-1],
            cls._rsi(stock_history).iloc[-1],
            cls._cvi(stock_history),
            cls._maximum_daily_return(stock_history).iloc[-1],
            cls._cho(stock_history).iloc[-1],
            cls._volatility(stock_history).iloc[-1],
            cls._turnover(stock_history).iloc[-1],
            cls._short_term_reversal(stock_history).iloc[-1],
            cls._vo(stock_history).iloc[-1],
            cls._absolute_return_to_volume(stock_history).iloc[-1],
            cls._cci(stock_history).iloc[-1],
            cls._imi(stock_history).iloc[-1],
            cls._idiosyncratic_volatility(stock_history, market_history),
            cls._capitalization_adjusted_turnover(stock_history).iloc[-1],
            cls._ar(stock_history).iloc[-1],
            cls._ddi(stock_history).iloc[-1],
            cls._coppock(stock_history).iloc[-1],
            cls._week52_high(stock_history).iloc[-1],
            cls._aroon(stock_history).iloc[-1],
            cls._cmo(stock_history).iloc[-1],
            cls._trading_turnover(stock_history).iloc[-1],
            # cls._market_ratio(stock_history, balance_sheet, shares_outstanding).iloc[-1],
            cls._dbcd(stock_history),
            cls._variation_of_share_turnover(stock_history).iloc[-1]
        ]
    
    @staticmethod
    def _daily_return(stock_history: pd.DataFrame) -> pd.DataFrame:
        daily_return = stock_history['Close'].pct_change()
        daily_return = daily_return.dropna()
        return daily_return

    @staticmethod
    def _market_cap(stock_history: pd.DataFrame) -> pd.DataFrame:
        market_cap = stock_history['Close'] * stock_history['Volume']
        return market_cap

    # BIAS 계산 함수
    # BIAS : 주가가 이동평균선에 대해 얼마나 괴리되어 있는지 백분율로 나타낸 값
    @staticmethod
    def _bias(stock_history: pd.DataFrame, window=20) -> pd.DataFrame:
        moving_avg = stock_history['Close'].rolling(window=window).mean()  # 이동평균선
        bias = (stock_history['Close'] - moving_avg) / moving_avg
        return bias

    # VMACD 계산 함수
    # 거래량 추세의 강도와 방향을 분석하는 데 사용
    @staticmethod
    def _vmacd(stock_history: pd.DataFrame, fast_window=12, slow_window=26, signal_window=9) -> tuple:
        fast_ema = stock_history['Volume'].ewm(span=fast_window, adjust=False).mean()  # 거래량 단기 EMA (Fast)
        slow_ema = stock_history['Volume'].ewm(span=slow_window, adjust=False).mean()  # 거래량 장기 EMA (Slow)

        macd = fast_ema - slow_ema  # MACD 선
        signal = macd.ewm(span=signal_window, adjust=False).mean()  # 신호선
        histogram = macd - signal  # 히스토그램
        return macd, signal, histogram

    @staticmethod
    def _rsi(stock_history: pd.DataFrame) -> pd.DataFrame:
        return ta.rsi(stock_history['Close'], length=14)

    @staticmethod
    def _cvi(stock_history: pd.DataFrame) -> np.float64:
        intraday_volatility = stock_history['High'] - stock_history['Low']
        cvi = intraday_volatility.std() / intraday_volatility.mean()
        return cvi

    @classmethod
    def _maximum_daily_return(cls, stock_history: pd.DataFrame) -> pd.DataFrame:
        daily_return = cls._daily_return(stock_history)
        maximum_daily_return = daily_return.rolling(window=len(daily_return)).max()
        return maximum_daily_return

    # ADL (Accumulation/Distribution Line) 계산
    @staticmethod
    def _adl(stock_history: pd.DataFrame) -> pd.DataFrame:
        mfm = ((stock_history['Close'] - stock_history['Low']) - (stock_history['High'] - stock_history['Close'])) / (stock_history['High'] - stock_history['Low'])
        mfv = mfm * stock_history['Volume']
        adl = mfv.cumsum()
        return adl

    # Chaikin Oscillator (CHO) 계산
    @classmethod
    def _cho(cls, stock_history: pd.DataFrame) -> pd.DataFrame:
        short_window = 3  # 단기 EMA
        long_window = 10  # 장기 EMA

        adl = cls._adl(stock_history)
        ema_short = adl.ewm(span=short_window, adjust=False).mean()
        ema_long = adl.ewm(span=long_window, adjust=False).mean()
        cho = ema_short - ema_long
        return cho

    @classmethod
    def _volatility(cls, stock_history: pd.DataFrame) -> pd.DataFrame:
        daily_return = cls._daily_return(stock_history)
        total_volatility = daily_return.rolling(window=len(daily_return)).std()
        return total_volatility

    @staticmethod
    def _turnover(stock_history: pd.DataFrame) -> pd.DataFrame:
        turnover = stock_history['Close'] * stock_history['Volume']
        turnover = turnover.dropna()

        # Average Turnover 계산 (거래대금의 평균)
        average_turnover = turnover.rolling(window=len(turnover)).mean()
        return average_turnover

    @classmethod
    def _short_term_reversal(cls, stock_history: pd.DataFrame) -> pd.DataFrame:
        daily_return = cls._daily_return(stock_history)

        # Short Term Reversal 계산 (5일 수익률의 음수 부호 반전)
        short_term_reversal = -daily_return.rolling(window=len(daily_return)).std()
        return short_term_reversal

    @staticmethod
    def _vo(stock_history: pd.DataFrame) -> pd.DataFrame:
        short_window = 5  # 단기 EMA 기간
        long_window = 20  # 장기 EMA 기간

        short_ma = stock_history['Volume'].rolling(window=short_window).mean()
        long_ma = stock_history['Volume'].rolling(window=long_window).mean()

        # VO (Volume Oscillator) 계산
        vo = ((short_ma - long_ma) / long_ma) * 100
        vo = vo.dropna()
        return vo

    @staticmethod
    def _absolute_return_to_volume(stock_history: pd.DataFrame) -> pd.DataFrame:
        # 절대 수익률 계산 (Absolute Return)
        absolute_return = abs(stock_history['Close'].pct_change())
        absolute_return = absolute_return.dropna()

        # Absolute Return to Volume 계산
        absolute_return_to_volume = absolute_return / stock_history['Volume']
        absolute_return_to_volume = absolute_return_to_volume.dropna()
        return absolute_return_to_volume

    @staticmethod
    def _cci(stock_history: pd.DataFrame) -> pd.DataFrame:
        cci = ta.cci(stock_history['High'], stock_history['Low'], stock_history['Close'], length=15)
        return cci

    # IMI 계산 (14일 기준)
    @staticmethod
    def _imi(stock_history: pd.DataFrame, day=14) -> pd.DataFrame:
        up_close = stock_history['Close'].diff() > 0
        down_close = stock_history['Close'].diff() < 0

        up_sum = stock_history['Close'].diff().where(up_close).fillna(0).rolling(window=day).sum()
        down_sum = stock_history['Close'].diff().where(down_close).fillna(0).rolling(window=day).sum()

        # IMI 계산
        imi = 100 * up_sum / (up_sum + down_sum)
        return imi

    @classmethod
    def _idiosyncratic_volatility(cls, stock_history: pd.DataFrame, market_history, period="6mo") -> np.float64:
        # 수익률 계산
        daily_return = cls._daily_return(stock_history)
        market_daily_return = market_history['Close'].pct_change().dropna()

        # 두 데이터프레임의 기간을 맞추기 위해 병합
        merged_data = pd.merge(daily_return, market_daily_return, left_index=True, right_index=True,
                               suffixes=('_asset', '_market'))
        merged_data = merged_data.dropna()

        # 회귀 분석을 통해 베타값과 알파값을 구합니다.
        model = LinearRegression()
        model.fit(merged_data['Close_market'].values.reshape(-1, 1), merged_data['Close_asset'])

        beta = model.coef_[0]
        alpha = model.intercept_

        # 자산의 예측 수익률 계산 (알파 + 베타 * 시장 수익률)
        predicted_returns = alpha + beta * merged_data['Close_market']
        # Idiosyncratic Volatility 계산: 자산의 실제 수익률에서 예측 수익률을 빼고, 그 표준편차를 구합니다.
        idiosyncratic_volatility = np.std(merged_data['Close_asset'] - predicted_returns)
        return idiosyncratic_volatility

    @classmethod
    def _capitalization_adjusted_turnover(cls, stock_history: pd.DataFrame) -> pd.DataFrame:
        market_cap = cls._market_cap(stock_history)
        capitalization_adjusted_turnover = stock_history['Volume'] / market_cap
        return capitalization_adjusted_turnover

    @staticmethod
    def _ar(stock_history: pd.DataFrame) -> pd.DataFrame:
        # A/D (Accumulation/Distribution) 지표 계산
        ad = ta.ad(stock_history['High'], stock_history['Low'], stock_history['Close'], stock_history['Volume'])

        # AR 계산: A/D의 누적값을 최대값으로 나누기
        ar = ad / ad.max()
        return ar

    @staticmethod
    def _ddi(stock_history: pd.DataFrame) -> pd.DataFrame:
        # True Range (TR) 계산
        previous_close = stock_history['Close'].shift(1)
        tr = pd.DataFrame({
            'High-Low': stock_history['High'] - stock_history['Low'],
            'High-PrevClose': (stock_history['High'] - previous_close).abs(),
            'Low-PrevClose': (stock_history['Low'] - previous_close).abs()
        }).max(axis=1)

        # ADX, +DI, -DI 계산
        adx = ta.adx(stock_history['High'], stock_history['Low'], stock_history['Close'])

        # +DI와 -DI를 정확하게 추출 (DMP_14 = +DI, DMN_14 = -DI)
        di_plus = adx['DMP_14']
        di_minus = adx['DMN_14']

        # DDI 계산: +DI와 -DI의 차이
        ddi = abs(di_plus - di_minus)
        return ddi

    # COPPOCK 지표 계산
    # 14일, 11일, 10일 EMA를 구하고 그 차이를 구함
    @staticmethod
    def _coppock(stock_history: pd.DataFrame) -> pd.DataFrame:
        coppock = ta.ema(stock_history['Close'], length=14) + ta.ema(stock_history['Close'], length=11) - ta.ema(stock_history['Close'], length=10)
        return coppock

    # Week52_High 계산
    @staticmethod
    def _week52_high(stock_history: pd.DataFrame) -> pd.DataFrame:
        week52_high = stock_history['High'].rolling(window=len(stock_history)).max()
        return week52_high

    @staticmethod
    def _aroon(stock_history: pd.DataFrame) -> pd.DataFrame:
        # AROON 계산 (최근 14일 기준)
        aroon = ta.aroon(stock_history['High'], stock_history['Low'], length=14)

        # AROON Up과 AROON Down 추출
        aroon_up = aroon['AROONU_14']
        aroon_down = aroon['AROOND_14']
        aroon = aroon_up - aroon_down
        return aroon

    @staticmethod
    def _cmo(stock_history: pd.DataFrame) -> pd.DataFrame:
        cmo = ta.cmo(stock_history['Close'], length=14)
        return cmo

    @classmethod
    def _trading_turnover(cls, stock_history: pd.DataFrame) -> pd.DataFrame:
        market_cap = cls._market_cap(stock_history)
        trading_turnover = stock_history['Volume'] / market_cap
        return trading_turnover

    # @staticmethod
    # def _market_ratio(stock_history: pd.DataFrame, balance_sheet, shares_outstanding) -> pd.DataFrame:
    #     # 'Total Liabilities' 계산 (단기 부채 + 장기 부채)
    #     total_current_liabilities = balance_sheet.loc['Current Liabilities']
    #     total_non_current_liabilities = balance_sheet.loc['Total Non Current Liabilities Net Minority Interest']
    #     total_liabilities = total_current_liabilities + total_non_current_liabilities
    #
    #     # 'Book Value of Equity' 계산 (자산 - 부채)
    #     total_assets = balance_sheet.loc['Total Assets']
    #     book_value_of_equity = total_assets - total_liabilities
    #
    #     # 주식 데이터 (시가총액 계산)
    #     market_price = stock_history['Close'].iloc[-1]  # 최신 종가
    #
    #     # 시가총액 계산
    #     market_value_of_equity = market_price * shares_outstanding
    #
    #     # Book to Market 계산
    #     book_to_market = book_value_of_equity / market_value_of_equity
    #     return book_to_market

    @staticmethod
    def _dbcd(stock_history: pd.DataFrame, period=14, history_period="1mo"):
        """
        DBCD 지표 계산법:
        - 매 거래일마다,
            + Close > Open 이면 +1,
            + Close < Open 이면 -1,
            + 둘이 같으면 0을 할당.
        - 그 후, 지정된 period(기본 14일) 동안의 이동평균을 계산.

        Parameters:
            period (int): 이동평균 기간 (default 14)
            history_period (str): yfinance에서 데이터를 가져올 기간 (예: "1mo")
        """
        # 각 거래일의 directional signal 계산: bullish (+1), bearish (-1), neutral (0)
        stock_history['direction'] = stock_history.apply(
            lambda row: 1 if row['Close'] > row['Open'] else (-1 if row['Close'] < row['Open'] else 0),
            axis=1
        )

        # 지정된 기간 동안의 이동평균(rolling mean) 계산 => DBCD 지표
        stock_history['DBCD'] = stock_history['direction'].rolling(window=period, min_periods=period).mean()

        # 계산된 DBCD 값 중 마지막 값 반환
        dbc_value = stock_history['DBCD'].iloc[-1]
        return dbc_value

    @staticmethod
    def _variation_of_share_turnover(stock_history: pd.DataFrame, window=20) -> pd.Series:
        """
        거래량 변동성 (Variation of Share Turnover) 계산 함수
        :param stock_history: DataFrame containing 'Volume' and 'Close'
        :param window: Rolling window size for turnover variation
        :return: Pandas Series with variation of share turnover
        """
        turnover = stock_history['Close'] * stock_history['Volume']
        variation = turnover.rolling(window=window).std() / turnover.rolling(window=window).mean()
        return variation
