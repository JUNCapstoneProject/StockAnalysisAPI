import pandas as pd
import hanlp


class TokenSRL:
    @staticmethod
    def labeling(tokens):
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

            verba0a1 = []
            for v in verb:
                for a0 in arg0:
                    for a1 in arg1:
                        verba0a1.append((v, a0, a1))

            # 각각의 역할에 대해 결과를 추출
            extracted_data.append({
                'verb': verb,
                'A0': arg0,
                'A1': arg1,
                'verba0a1': verba0a1
            })

        df = pd.DataFrame(extracted_data)
        return df
