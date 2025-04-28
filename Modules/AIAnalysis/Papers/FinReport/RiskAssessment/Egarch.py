import numpy as np
from arch import arch_model


class VaR:
    def __init__(self, data):
        self.data = self._preprocessing(data)
        self.model = self._model(self.data)
        self.confidence_level = 0.99

    def forecast(self):
        forecast = self.model.forecast(horizon=1)
        forecast_mean = forecast.mean.iloc[-1, 0]
        forecast_variance = forecast.variance.iloc[-1, 0]
        forecast_vol = np.sqrt(forecast_variance)

        # VaR 계산 (신뢰수준 99% 기준)
        z_alpha = -2.33  # 정규분포 1% quantile
        VaR = -forecast_mean - z_alpha * forecast_vol
        return VaR

    def _model(self, data):
        returns = data["Returns"].values

        # 학습/테스트 데이터 분할 (전체 80%는 학습, 20%는 테스트)
        n = len(returns)

        p, q = 1, 1  # EGARCH(1, 1)
        z_alpha = -2.33  # 정규분포 1% quantile

        VaR_forecasts = []
        forecast_dates = []

        # 새로운 데이터가 추가될 때마다 모델을 업데이트(재학습)
        model_fit = None
        for t in range(n):
            # 시점 t 이전(0 ~ t-1)의 데이터를 사용해 모델 적합
            model = arch_model(returns[:t], vol='EGARCH', p=p, q=q, dist='normal')
            model_fit = model.fit(disp="off")

            # 다음 시점 t에 대한 예측
            forecast = model_fit.forecast(horizon=1)
            mean_forecast = forecast.mean.iloc[-1, 0]
            vol_forecast = np.sqrt(forecast.variance.iloc[-1, 0])

            # VaR = -(예측 기대수익률 - z_alpha * 변동성)
            VaR_t = -(mean_forecast + z_alpha * vol_forecast)
            VaR_forecasts.append(VaR_t)
            forecast_dates.append(data.index[t])

        return model_fit

    def _preprocessing(self, data):
        data["Returns"] = data["Close"].pct_change()
        data.dropna(inplace=True)
        return data
