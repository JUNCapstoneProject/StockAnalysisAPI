from Modules.AIAnalysis.pipeline import pipeline
# 임시 모듈
from Datas.News.bbc import news, news_cn
from Datas.Stock.Yfinance import GetYfinance

data = {
    'news_data': news_cn
}
pipeline('news', data)
