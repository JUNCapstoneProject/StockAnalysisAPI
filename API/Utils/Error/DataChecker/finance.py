from datetime import datetime
# bridge
from API.Utils.Error.DataChecker.common import df_checker
from Utils.Error.UserError import UserInputError


def lstm_checker(data):
    """문제가 없으면 True 반환, 문제가 있으면 UserInputError 발생"""
    timestamps = data["chart"]["timestamp"]
    # 1. 포맷 검사 및 datetime 객체로 변환
    parsed_dates = []
    for ts in timestamps:
        try:
            dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
            parsed_dates.append(dt)
        except ValueError:
            raise UserInputError('timestamp 형식이 잘못된 데이터가 존재합니다')

    # 2. 오름차순 정렬 여부 확인
    is_sorted = all(parsed_dates[i] <= parsed_dates[i + 1] for i in range(len(parsed_dates) - 1))
    if is_sorted:
        pass
    else:
        raise UserInputError('데이터가 정렬되지 않았습니다')

    # 3. 데이터 중복 확인
    duplicates = set([ts for ts in timestamps if timestamps.count(ts) > 1])
    if duplicates:
        raise UserInputError("중복된 timestamp가 있습니다:")
    else:
        pass

    # 4. 데이터 갯수 확인
    # 4.1 데이터 공백 확인
    if parsed_dates:
        pass
    else:
        raise UserInputError("데이터가 비어있습니다")

    # 4.2 최소 1년치 데이터 여부 확인
    date_range = (max(parsed_dates) - min(parsed_dates)).days
    if date_range >= 365:
        pass
    else:
        raise UserInputError("1년치 이상의 데이터가 필요합니다")

    # 4.3 재무제표 데이터프레임 생성 가능성 확인
    # 각 데이터들이 모두 데이터프레임 생성 가능해야 True 반환
    return (df_checker(data['balance_sheet'])
            and df_checker(data['income_statement'])
            and df_checker(data['cash_flow'])
            and df_checker(data['chart']))
