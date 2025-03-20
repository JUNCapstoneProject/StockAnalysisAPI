from AutoTrading.pipeline import pipeline
# 임시 모듈
from Datas.News.bbc import news, news_cn
from Datas.Stock.Yfinance import GetYfinance

data = {
    'news_data': news_cn
}
pipeline('news', data)

host = "msiwol.iptime.org"
message = {
    "header": {
        "Host": host,
        "Origin": f"https://{host}",
        "Referer": f"https://{host}/api/analysis/crawling/distributor/notifier",
        "Request URL": f"https://{host}/api/analysis/stock/pipeline",
        "Request Method": "GET",
        "Authorization": "",
    },
    "body": {
        "items": [
            {
                "title": "...",
                "organization": "bbc",
                "url": "...",
                "posted_at": "...",
                "contents": ""
            }
        ]
    }
}