import functools
import pandas as pd


def adapter(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if len(args) >= 2:  # 위치 인자로 전달된 경우
            data = args[1]
        else:  # 키워드 인자로 전달된 경우
            data = kwargs.get('data', False)

        if isinstance(data['stock_history'], pd.DataFrame):  # 이미 변환이 되있음
            return func(*args, **kwargs)
        else:
            stock_history_df = pd.DataFrame(data['stock_history'])
            market_history_df = pd.DataFrame(data['market_history'])
            income_statement_df = pd.DataFrame(data['income_statement'])
            info_df = pd.DataFrame(data['info'])

            stock_history_df = stock_history_df.apply(pd.to_numeric, errors='ignore')
            market_history_df = market_history_df.apply(pd.to_numeric, errors='ignore')
            income_statement_df = income_statement_df.apply(pd.to_numeric, errors='ignore')
            info_df = info_df.apply(pd.to_numeric, errors='ignore')
            """
            # 나중에 chart['timestamp'].dt 해야함
            # 반드시 .apply(pd.to_numeric)를 거친 뒤에 to_datetime을 해줘야 함
            """
            stock_history_df['Date'] = pd.to_datetime(stock_history_df['Date'])
            market_history_df['Date'] = pd.to_datetime(market_history_df['Date'])

            data = {
                'news_data': data['news_data'],
                'stock_history': stock_history_df,
                'market_history': market_history_df,
                'income_statement': income_statement_df,
                'info': info_df
            }
            if len(args) >= 2:  # 위치 인자로 전달된 경우
                args = list(args)
                args[1] = data
                return func(*args, **kwargs)
            else:  # 키워드 인자로 전달된 경우
                kwargs.pop('data', None)
                return func(*args, **kwargs, data=data)

    return wrapper
