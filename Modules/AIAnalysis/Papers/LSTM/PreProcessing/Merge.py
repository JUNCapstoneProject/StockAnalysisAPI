import pandas as pd
import numpy as np


def merge(finance_feature, chart):
    finance_feature['date'] = pd.to_datetime(finance_feature.index)
    chart['date'] = pd.to_datetime(chart.index)

    start_date = finance_feature['date'].min()

    # chart에서 start_date부터 end_date 사이의 날짜만 필터링
    chart_filtered = chart[(chart['date'] >= start_date)]

    # 더미 행 추가 (start_date 날짜가 chart에 없는 경우 대비)
    dummy_row = {col: np.nan for col in chart_filtered.columns}
    dummy_row['date'] = start_date
    #     chart_filtered = chart_filtered.append(dummy_row, ignore_index=True)
    chart_filtered = pd.concat([chart_filtered, pd.DataFrame([dummy_row])], ignore_index=True)

    merged_data = chart_filtered.copy()

    # 'finance_feature'의 값을 'chart_filtered'에 적용
    for date in finance_feature['date'].unique():
        row_values = finance_feature.loc[finance_feature['date'] == date].drop(columns='date')
        merged_data.loc[merged_data['date'] == date, row_values.columns] = row_values.values

    # 정렬, NaN & 중복 값 처리
    merged_data.sort_values(by='date', inplace=True)
    merged_data.fillna(method='ffill', inplace=True)
    merged_data.drop_duplicates(inplace=True)
    merged_data.dropna(inplace=True)
    return merged_data
