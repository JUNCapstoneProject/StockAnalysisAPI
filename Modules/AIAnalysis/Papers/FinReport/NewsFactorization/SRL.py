import os
from transformers import BertTokenizer
from collections import Counter
import pandas as pd
import numpy as np
import hanlp

file_path = os.path.abspath(__file__)
directory = os.path.dirname(file_path)


class TokenSRL:
    TOKENIZER_DIR = os.path.join(directory, '../../../Models/ROBERT_4_model.bin')
    TOKENIZER_DIR = os.path.normpath(TOKENIZER_DIR)

    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained(self.TOKENIZER_DIR)

    def labeling(self, news_data):
        tokens = self.tokenizer.tokenize(news_data)

        """tokenizer를 거친 tokens가 필요"""
        srl_model = hanlp.load('CPB3_SRL_ELECTRA_SMALL')
        srl_result = srl_model([tokens])

        extracted_data = []
        for sentence in srl_result:
            verb = []
            arg0 = []
            arg1 = []

            # 각 sentence 내의 항목 처리
            for item in sentence:
                for word, role, start, end in item:
                    if role == 'PRED':  # 동사(PRED) 추출
                        verb.append((start, end))
                    elif role == 'ARG0':  # 주어(ARG0) 추출
                        arg0.append((start, end))
                    elif role == 'ARG1':  # 목적어(ARG1) 추출
                        arg1.append((start, end))

            # 각 문장에서 verb, arg0, arg1의 조합을 만들기
            verbA0A1 = []
            for v in verb:
                verb_a0a1 = []
                for a0 in arg0:
                    for a1 in arg1:
                        verb_a0a1.append((v, a0, a1))  # verb, arg0, arg1의 조합을 추가
                verbA0A1.append(verb_a0a1)  # 한 문장에서의 verbA0A1 목록을 추가

            # 각 문장에 대한 결과 추출
            extracted_data.append({
                'verb': verb,
                'A0': arg0,
                'A1': arg1,
                'verbA0A1': verbA0A1
            })

        df = pd.DataFrame(extracted_data)
        return self.mask(df)

    # def mask(self, df) -> pd.DataFrame:
    #     df = df.reset_index(drop=True)
    #     df['verb_mask'] = 0
    #     df['A0_mask'] = 0
    #     df['A1_mask'] = 0
    #     df['verb_mask'] = df['verb_mask'].astype('object')
    #     df['A0_mask'] = df['A0_mask'].astype('object')
    #     df['A1_mask'] = df['A1_mask'].astype('object')
    #     for index, row in df.iterrows():
    #         AV_num = 0
    #         for k, col in enumerate(['verb', 'A0', 'A1']):
    #             masks = []
    #             for j in range(len(row['verbA0A1'])):
    #                 mask = np.zeros(299)
    #                 idx = []
    #                 for v in row['verbA0A1'][j][k]:
    #                     idx = idx + [int(i) for i in range(v[0], v[0] + v[1])]
    #
    #                 # idx = np.unique(idx).tolist()
    #                 counter = Counter(idx)
    #                 mask = [0 if counter[i] == 0 else 1 / len(counter) for i in range(0, len(mask))]
    #                 mask.insert(0, 0)
    #                 masks.append(mask)
    #
    #             AV_num = len(masks)
    #             for i in range(10 - len(masks)):
    #                 masks.append(np.zeros(300))
    #
    #             while len(masks) > 10:
    #                 masks.pop()
    #
    #             name = col + '_mask'
    #             df.at[index, name] = np.array(masks)
    #
    #         if AV_num > 10:
    #             AV_num = 10
    #
    #         df.loc[index, 'AV_num'] = int(AV_num)
    #
    #     df.AV_num = df.AV_num.astype('int')
    #     return df

    def mask(self, df) -> dict:
        df = df.reset_index(drop=True)
        output = {
            'verb_mask': [],
            'A0_mask': [],
            'A1_mask': [],
            'AV_num': []
        }

        for index, row in df.iterrows():
            AV_num = 0
            row_masks = {'verb_mask': None, 'A0_mask': None, 'A1_mask': None}

            for k, col in enumerate(['verb', 'A0', 'A1']):
                masks = []
                for j in range(len(row['verbA0A1'])):
                    mask = np.zeros(299)
                    idx = []
                    for v in row['verbA0A1'][j][k]:
                        idx += [int(i) for i in range(v[0], v[0] + v[1])]

                    counter = Counter(idx)
                    mask = [0 if counter[i] == 0 else 1 / len(counter) for i in range(0, len(mask))]
                    mask.insert(0, 0)
                    masks.append(mask)

                AV_num = len(masks)
                for i in range(10 - len(masks)):
                    masks.append(np.zeros(300))

                while len(masks) > 10:
                    masks.pop()

                row_masks[f'{col}_mask'] = np.array(masks)

            if AV_num > 10:
                AV_num = 10

            # Append to output dictionary
            output['verb_mask'].append(row_masks['verb_mask'])
            output['A0_mask'].append(row_masks['A0_mask'])
            output['A1_mask'].append(row_masks['A1_mask'])
            output['AV_num'].append(np.array([int(AV_num)]))

        return output
