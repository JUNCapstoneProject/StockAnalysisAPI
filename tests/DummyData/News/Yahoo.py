import os
import pandas as pd
from API.Socket.Messages.request import requests_message, news_item

file_path = os.path.abspath(__file__)
directory = os.path.dirname(file_path)

DATA_PATH = os.path.join(directory, 'test_news_stock_data.csv')


def get_message():
    # 테스트 메세지 준비
    test_message = requests_message
    test_item = get_item()
    test_message['body']['item'] = test_item
    return test_message


def get_item():
    # 테스트 아이템 준비
    news_df = pd.read_csv(DATA_PATH)
    test_item = news_item
    test_item['data']['news_data'] = get_news(news_df)
    test_item['data']['stock_history'] = get_stock_history(news_df)
    test_item['data']['market_history'] = get_market_history(news_df)
    # TODO : Return Forecasting (unused) Module 개발 시 아래 데이터들도 필요
    # test_item['data']['income_statement'] = get_income_statement(news_df)
    # test_item['data']['info'] = get_info(news_df)
    return test_item


def get_news(news_df):
    return [news_df['script'][0]]


def get_stock_history(news_df):
    # FIXME : Market Cap은 원본 데이터셋에 있어야 하지 않을까?
    # FIXME : 원래 1개의 stock에 대해 30일치의 주가 데이터가 필요한게 맞음
    # news_df = news_df.iloc[:2]
    # market_cap = news_df.xs('Adj Close', level=0, axis=1).multiply(news_df.xs('Volume', level=0, axis=1))
    # for ticker in market_cap.columns:
    #     news_df[('Market Cap', ticker)] = market_cap[ticker]

    return {
        'stock': news_df['stock'][:30].tolist(),
        'Date': news_df['date'][:30].tolist(),
        'Open': news_df['Open'][:30].tolist(),
        'Close': news_df['Close'][:30].tolist(),
        'High': news_df['High'][:30].tolist(),
        'Low': news_df['Low'][:30].tolist(),
        'Volume': news_df['Volume'][:30].tolist(),
        # 'Market Cap': news_df['Market Cap'].tolist()
    }


def get_market_history(news_df):
    # FIXME : 얘도 Volume, Market Cap 필요한가?
    return {
        'm_Symbol': news_df['m_Symbol'][:30].tolist(),
        'Date': news_df['date'][:30].tolist(),
        'Open': news_df['m_Open'][:30].tolist(),
        'Close': news_df['m_Close'][:30].tolist(),
        'High': news_df['m_High'][:30].tolist(),
        'Low': news_df['m_Low'][:30].tolist()
    }


def get_income_statement(news_df):
    return {
        "Total Revenue": news_df["Total Revenue"][:30].tolist(),
        'Normalized Income': news_df['Normalized Income'][:30].tolist(),
    }


def get_info(news_df):
    return {
        "priceToBook": news_df['priceToBook'][:30].tolist()
    }
