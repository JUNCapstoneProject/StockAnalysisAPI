# Bridge
from Modules.Utils.Socket.Web.Decorator import *
from Modules.AIAnalysis.pipeline import pipeline


@RequestMapping('/stock')
class StockPriceForecastingController:
    @GetMapping('/pipeline')
    def forecasting(self, event_type, data):
        return pipeline(event_type, data)
