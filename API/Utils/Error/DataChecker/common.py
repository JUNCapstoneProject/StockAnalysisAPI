

def df_checker(d) -> bool:
    """해당 딕셔너리로 데이터프레임 생성이 가능한지"""
    # 빈 딕셔너리는 True로 간주
    if not d:
        return True

    # 모든 값이 리스트인지 확인
    if not all(isinstance(v, list) for v in d.values()):
        return False

    # 모든 리스트의 길이가 같은지
    lengths = [len(v) for v in d.values()]
    return all(length == lengths[0] for length in lengths)
