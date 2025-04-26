# bridge
from Modules.Utils.Interfaces.Pipeline import Input
# NewsFactorization
from Modules.AIAnalysis.Papers.FinReport.NewsFactorization import NewsFactorInput
# ReturnForecasting
from Modules.AIAnalysis.Papers.FinReport.ReturnForecasting.StockFactor import QuantitativeFactor


class ForecastingInput(Input):
    def __init__(self):
        pass

    def __call__(self, data):
        quantitative_factor = QuantitativeFactor.create_factor(data['stock_data'], data['market_data'])