from datetime import datetime
# bridge
from API.Utils.Error.DataChecker.common import df_checker
from Utils.Error.UserError import UserInputError


def _validate_dates(dates, label):
    try:
        return [datetime.strptime(ts, "%Y-%m-%d") for ts in dates]
    except ValueError:
        raise UserInputError(f'{label}에 Date 형식이 잘못된 데이터가 존재합니다')


def _is_sorted(parsed_dates):
    is_sorted = all(parsed_dates[i] <= parsed_dates[i + 1] for i in range(len(parsed_dates) - 1))
    is_sorted_desc = all(parsed_dates[i] >= parsed_dates[i + 1] for i in range(len(parsed_dates) - 1))
    if is_sorted or is_sorted_desc:
        pass
    else:
        raise UserInputError('데이터가 정렬되지 않았습니다')


def _is_duplicated(timestamps):
    # duplicates = set([ts for ts in timestamps if timestamps.count(ts) > 1])
    # if duplicates:
    #     raise UserInputError("중복된 timestamp가 있습니다:")
    # else:
    #     pass
    pass


def sentiment_classifier_checker(data):
    stock_dates = data['stock_history']['Date']
    market_dates = data['market_history']['Date']

    # 1. 포맷 검사 및 datetime 객체로 변환
    parsed_stock_dates = _validate_dates(stock_dates, 'stock_history')
    parsed_market_dates = _validate_dates(market_dates, 'market_history')

    # 2. 오름차순 정렬 여부 확인
    _is_sorted(parsed_stock_dates)
    _is_sorted(parsed_market_dates)

    # 3. 데이터 중복 확인
    _is_duplicated(stock_dates)
    _is_duplicated(market_dates)

    # 4. 데이터 갯수 확인
    # 4.1 데이터 공백 확인
    if parsed_stock_dates and parsed_market_dates:
        pass
    else:
        raise UserInputError("데이터가 비어있습니다")

    # 4.2 최소 1년치 데이터 여부 확인
    date_stock_range = (max(parsed_stock_dates) - min(parsed_stock_dates)).days
    date_market_range = (max(parsed_market_dates) - min(parsed_market_dates)).days
    if (date_stock_range >= 15) and (date_market_range >= 15):
        pass
    else:
        raise UserInputError("15일치 이상의 데이터가 필요합니다")

    # 4.3 재무제표 데이터프레임 생성 가능성 확인
    # 각 데이터들이 모두 데이터프레임 생성 가능해야 True 반환
    return (df_checker(data['stock_history'])
            and df_checker(data['market_history']))
