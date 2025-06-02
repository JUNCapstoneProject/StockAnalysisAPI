from API.Socket.Messages.request import *
from API.Utils.Error.DataChecker.finance import *
from API.Utils.Error.DataChecker.news import *


def _get_origin_item(event_type):
    if event_type == 'news':
        return news_item
    elif event_type == 'finance':
        return finance_item


def _get_item_checker(path):
    """item_checker라는 함수 반환"""
    if path == '/finance/lstm':
        return lstm_checker
    elif path == '/news/sentiment_classifier':
        return sentiment_classifier_checker


def _extract_keys(d, prefix=''):
    """중첩된 딕셔너리의 키들까지 모두 prefix.key 형식으로 추출"""
    keys = set()
    for key, value in d.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            keys.update(_extract_keys(value, full_key))
        else:
            keys.add(full_key)
    return keys


def data_check(path, data: dict) -> bool:
    """
    request_message['body']['item']['data'] 검사
    request_path는 /news/sentiment_classifier 이런 형식
    각 api에 해당하는 checker를 호출하여 검사
    """
    event_type = path.split('/')[1]
    origin_item = _get_origin_item(event_type)
    origin_data = origin_item['data']
    # 메세지 구조 검사
    if event_type == 'finance' and (_extract_keys(origin_data) == _extract_keys(data)):
        item_checker = _get_item_checker(path)
        return item_checker(data)
    elif event_type == 'news' and (_extract_keys(origin_data) >= _extract_keys(data)):
        item_checker = _get_item_checker(path)
        return item_checker(data)
    else:
        print('있어야 할 데이터 :', _extract_keys(origin_data) - _extract_keys(data))
        print('있어선 안 될 데이터 :', _extract_keys(data) - _extract_keys(origin_data))
        raise UserInputError("메세지 구조가 올바르지 않음")
