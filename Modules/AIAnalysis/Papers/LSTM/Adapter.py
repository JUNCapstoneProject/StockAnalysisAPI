import functools
import pandas as pd


def adapter(func):
    # adpater가 발생시킨 에러는 memoize 데코레이터가 처리
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # data 가져오기
        if len(args) >= 2:  # 위치 인자로 전달된 경우
            data = args[1]
        elif 'data' in kwargs:  # 키워드 인자로 전달된 경우
            data = kwargs.get('data', None)  # data=None 처럼 이상한거 전달할 경우
        else:  # 아예 전달이 안 됨
            raise Exception('data를 넘겨받지 못함')

        # data 가공하기
        if isinstance(data['chart'], pd.DataFrame):  # 이미 변환이 되있음
            return func(*args, **kwargs)
        elif data:  # 키워드 인자로 유효한 데이터를 넘겨받았다면
            processed_data = process_data(data)
        else:  # data=None 처럼 넘겨받음
            raise Exception('유효하지 않은 data')

        # data 반환하기 (data가 가공된 경우에만)
        if len(args) >= 2:  # 위치 인자로 전달된 경우
            args = list(args)
            args[1] = processed_data
            return func(*args, **kwargs)
        else:  # 키워드 인자로 전달된 경우
            kwargs.pop('data', None)
            return func(*args, **kwargs, data=processed_data)

    return wrapper


def process_data(data):
    try:
        chart_df = pd.DataFrame(data['chart'])
        balance_sheet_df = pd.DataFrame(data['balance_sheet'])
        income_statement_df = pd.DataFrame(data['income_statement'])
        cash_flow_df = pd.DataFrame(data['cash_flow'])
    except KeyError as keyword:
        raise KeyError(f'data에 key {keyword}이/가 포함되어 있지 않음')
    else:
        chart_df = chart_df.apply(pd.to_numeric, errors='ignore')
        balance_sheet_df = balance_sheet_df.apply(pd.to_numeric, errors='ignore')
        income_statement_df = income_statement_df.apply(pd.to_numeric, errors='ignore')
        cash_flow_df = cash_flow_df.apply(pd.to_numeric, errors='ignore')
        """
        # 나중에 chart['timestamp'].dt 해야함
        # 반드시 .apply(pd.to_numeric)를 거친 뒤에 to_datetime을 해줘야 함
        """
        chart_df['timestamp'] = pd.to_datetime(chart_df['timestamp'])

        return {
            'chart': chart_df,
            'balance_sheet': balance_sheet_df,
            'income_statement': income_statement_df,
            'cash_flow': cash_flow_df
        }
