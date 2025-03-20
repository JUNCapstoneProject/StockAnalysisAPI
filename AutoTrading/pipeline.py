import pandas as pd
#
# Modules
from Modules.FinReport import Input as FinReportInput


def pipeline(event_type, data):
    module_num = event_mapping(event_type)
    feature_map = create_feature(module_num, data)
    y_hat = stock_predict(feature_map)

def event_mapping(event_type) -> int:
    mapping = {
        'news': 1
    }
    return mapping[event_type]


def create_feature(module_num, data) -> pd.Series:
    fin_input = FinReportInput(data)
    fin_output = fin_input(module_num==1)
    return pd.Series()


def stock_predict(feature_map) -> float:
    pass

