import os
import pandas as pd
from Modules.Utils.Socket.Messages.request import requests_message, finance_item

file_path = os.path.abspath(__file__)
directory = os.path.dirname(file_path)

CHART_PATH = os.path.join(directory, 'test_chart.csv')
BALANCE_SHEET_PATH = os.path.join(directory, 'test_balance_sheet.csv')
INCOME_STATEMENT_PATH = os.path.join(directory, 'test_income_statement.csv')
CASH_FLOW_PATH = os.path.join(directory, 'test_cash_flow.csv')


def get_message():
    # 테스트 메세지 준비
    test_message = requests_message
    test_item = get_item()
    test_message['body']['item'] = test_item
    return test_message


def get_item():
    # 테스트 아이템 준비
    test_item = finance_item
    # 테스트 차트
    test_item['data']['chart'] = get_chart()
    # 테스트 재무제표
    balance_sheet, income_statement, cash_flow = get_finance()
    test_item['data']['balance_sheet'] = balance_sheet
    test_item['data']['income_statement'] = income_statement
    test_item['data']['cash_flow'] = cash_flow
    return test_item


def get_chart():
    # 테스트 데이터 준비
    test_data = pd.read_csv(CHART_PATH)
    test_data.dropna(inplace=True)
    return {
        "timestamp": test_data['Date'].tolist(),
        # "v": data['Volume'].tolist(),  # Volume
        # "vw": data['Adj Close'].rolling(window=5).mean().tolist(),  # Volume Weighted Average Price (5일 이동 평균 예시)
        "o": test_data['Open'].tolist(),  # Open
        "c": test_data['Close'].tolist(),  # Close
        # "h": data['High'].tolist(),    # High
        # "l": data['Low'].tolist(),     # Low
        # "t": data.index.strftime('%Y-%m-%d').tolist(),  # Time (날짜 형식)
        # "n": None  # Number of trades (yfinance에는 직접적인 거래 수 데이터를 제공하지 않으므로 None으로 채움)
    }


def get_finance():
    balance_sheet = pd.read_csv(BALANCE_SHEET_PATH, index_col=0).T
    income_statement = pd.read_csv(INCOME_STATEMENT_PATH, index_col=0).T
    cash_flow = pd.read_csv(CASH_FLOW_PATH, index_col=0).T
    return {
        "Current Assets": [balance_sheet['Current Assets'][0]],
        "Current Liabilities": [balance_sheet['Current Liabilities'][0]],
        "Cash And Cash Equivalents": [balance_sheet['Cash And Cash Equivalents'][0]],
        "Accounts Receivable": [balance_sheet['Accounts Receivable'][0]],
        "Cash Cash Equivalents And Short Term Investments": [
            balance_sheet['Cash Cash Equivalents And Short Term Investments'][0]],
        "Cash Equivalents": [balance_sheet['Cash Equivalents'][0]],
        "Cash Financial": [balance_sheet['Cash Financial'][0]],
        "Other Short Term Investments": [balance_sheet['Other Short Term Investments'][0]],
        "Stockholders Equity": [balance_sheet['Stockholders Equity'][0]],
        "Total Assets": [balance_sheet['Total Assets'][0]],
        "Retained Earnings": [balance_sheet['Retained Earnings'][0]],
        "Inventory": [balance_sheet['Inventory'][0]]
    }, {
        "Total Revenue": [income_statement['Total Revenue'][0]],
        "Cost Of Revenue": [income_statement['Cost Of Revenue'][0]],
        "Gross Profit": [income_statement['Gross Profit'][0]],
        "Selling General And Administration": [income_statement['Selling General And Administration'][0]],
        "Operating Income": [income_statement['Operating Income'][0]],
        "Other Non Operating Income Expenses": [income_statement['Other Non Operating Income Expenses'][0]],
        "Reconciled Depreciation": [income_statement['Reconciled Depreciation'][0]],
        "EBITDA": [income_statement['EBITDA'][0]]
    }, {
        "Operating Cash Flow": [cash_flow['Operating Cash Flow'][0]],
        "Investing Cash Flow": [cash_flow['Investing Cash Flow'][0]],
        "Capital Expenditure": [cash_flow['Capital Expenditure'][0]]
    }


if __name__ == "__main__":
    import yfinance as yf

    # 'MSFT' 티커에 대한 데이터를 다운로드 (오늘로부터 10일 전까지)
    ticker = 'MSFT'
    # data = yf.history(ticker, period='10d', interval='1d')
    ticker = yf.Ticker(ticker)
    data = ticker.history(period='365d')
    data.to_csv(CHART_PATH)
    # ticker = yf.Ticker(ticker)
    # balance_sheet = ticker.balance_sheet.T.iloc[0]
    # income_statement = ticker.income_stmt.T.iloc[0]
    # cash_flow = ticker.cash_flow.T.iloc[0]
    # balance_sheet.to_csv(BALANCE_SHEET_PATH)
    # income_statement.to_csv(INCOME_STATEMENT_PATH)
    # cash_flow.to_csv(CASH_FLOW_PATH)
