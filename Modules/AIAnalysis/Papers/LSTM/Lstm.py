import os
import numpy as np
import tensorflow as tf

file_path = os.path.abspath(__file__)
directory = os.path.dirname(file_path)


class FinanceLSTM:
    LSTM_DIR = os.path.join(directory, '../../../AIAnalysis/Models/finance_lstm.h5')
    LSTM_DIR = os.path.normpath(LSTM_DIR)

    def __init__(self):
        self.model = tf.keras.models.load_model(self.LSTM_DIR)

    def prediction(self, merged_df) -> int:
        """
        0이 부정, 1이 긍정 신호
        """
        merged_df.drop(columns=['date'], inplace=True)
        merged_df = merged_df.drop(columns=['IntraR-future', 'label']).values.astype(np.float32)
        merged_df = self.reshaper(merged_df)
        prediction = self.model.predict(merged_df)[-1]  # 성능 테스트 할 땐 [-1] 주석처리 해야 함
        # return prediction[:, 0]  # 성능 테스트 할 땐 이걸 return해야 함
        prediction_class = list(prediction).index(max(prediction))
        return prediction_class

    @staticmethod
    def reshaper(arr):
        # arr를 3개의 채널로 나누고 축을 교환하여 (샘플, 타임스텝, 채널) 형태로 변경
        arr = np.array(np.split(arr, 3, axis=1))
        arr = np.swapaxes(arr, 0, 1)
        arr = np.swapaxes(arr, 1, 2)
        return arr.astype(np.float32)
