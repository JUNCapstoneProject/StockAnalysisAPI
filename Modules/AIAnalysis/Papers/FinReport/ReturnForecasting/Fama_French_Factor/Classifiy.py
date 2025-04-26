import pandas as pd


class ClassifiyCompanies:
    @staticmethod
    def by_pb(pb_data, quantile=0.3):
        """
        P/B 비율을 기준으로 기업을 High(상위)와 Low(하위)로 구분합니다.
        :param pb_data: 각 기업의 P/B 비율 데이터
        :param quantile: 상위/하위 몇 퍼센트를 기준으로 구분할지
        :return: High(상위) 기업과 Low(하위) 기업 리스트
        """
        high_threshold = pb_data.quantile(1 - quantile)  # 상위 30%
        low_threshold = pb_data.quantile(quantile)  # 하위 30%

        high_pb = pb_data[pb_data >= high_threshold].index.tolist()  # P/B 상위 30%
        low_pb = pb_data[pb_data <= low_threshold].index.tolist()  # P/B 하위 30%
        return high_pb, low_pb

    @staticmethod
    def by_capex(capex_data, quantile_ratio=0.3):
        """
        CapEx 데이터로 기업들을 상위 30%와 하위 30%로 구분합니다.
        :param capex_data: 각 기업의 CapEx 데이터
        :param quantile_ratio: 하위 30%를 기준으로 분할할 비율
        :return: 상위 30% (aggressive)와 하위 30% (conservative) 기업 목록
        """
        # 시리즈 데이터에서 숫자형으로 변환
        flattened_data = pd.DataFrame.from_dict({key: val for key, val in capex_data.items()}, orient='index')
        flattened_data = flattened_data.stack().reset_index(drop=True)  # 데이터 평탄화
        capex_data = pd.to_numeric(flattened_data, errors="coerce").dropna()

        # CapEx 데이터의 상위 30%와 하위 30% 계산
        n_aggressive = int(len(capex_data) * (1 - quantile_ratio))  # 상위 30% 개수
        n_conservative = int(len(capex_data) * quantile_ratio)  # 하위 30% 개수

        # 상위 30%와 하위 30%를 nlargest와 nsmallest로 구하기
        aggressive = capex_data.nlargest(n_aggressive)  # 상위 30%
        conservative = capex_data.nsmallest(n_conservative)  # 하위 30%
        return aggressive, conservative
