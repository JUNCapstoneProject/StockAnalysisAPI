from transformers import BertTokenizer, AutoModelForTokenClassification
import pandas as pd
import torch
import hanlp
# import json
# import spacy
import os
# bridge

# from Modules.Azure.ml import EndPoints
# from Models.SimpleSentimentModel import SimpleSentimentModel


class NewsTokenizer:
    ENDPOINTS_URL = 'https://tokenizer-endpoint-3ff719b6.koreacentral.inference.ml.azure.com/score'
    TOKENIZER_DIR = r'C:\Users\black\Desktop\DevTools\Projects\Capstone\StockMarketAnalysis\Models\ROBERT_4_model.bin'

    @classmethod
    def tokenization(cls, news_data):
        # cls._azureml(news_data)
        return cls._extract_roles(news_data)

    # ROBERT(local) 기반 tokenizer(cn)
    @classmethod
    def _extract_roles(cls, text):
        """
        입력 텍스트에서 A0(Agent), A1(Patient), VerbA0A1(동사)의 위치를 추출하는 함수
        RoBERTa 기반 모델을 사용하여 역할을 예측함
        """
        tokenizer = BertTokenizer.from_pretrained(cls.TOKENIZER_DIR)
        tokens = tokenizer.tokenize(text)
        return tokens

    # ROBERT(azureml) 기반 tokenizer(cn)
    # @classmethod
    # def _extract_roles(cls, text):
    #     df = EndPoints.request(endpoints_url=cls.ENDPOINTS_URL, data={
    #         "data": text
    #     })
    #     return df

    # spacy 기반 tokenizer(en) (decrypted)
    # @staticmethod
    # def _extract_roles(text):
    #     """
    #     입력 텍스트에서 A0(Agent), A1(Patient), VerbA0A1(동사)의 위치를 추출하는 함수
    #     """
    #     nlp = spacy.load("en_core_web_sm")
    #     doc = nlp(text)
    #
    #     # 위치 정보를 저장할 리스트
    #     verb_info_list = []
    #     a0_info_list = []
    #     a1_info_list = []
    #     verb_a0a1_info_list = []
    #
    #     # 모든 동사와 관련된 의존 관계 탐색
    #     for token in doc:
    #         if token.pos_ == "VERB":  # 동사를 발견
    #             verb_info = (token.idx, token.idx + len(token.text) - 1)
    #             verb_info_list.append(verb_info)
    #
    #             a0_info = []
    #             a1_info = []
    #
    #             # A0 (Agent): 동사의 주어
    #             for child in token.children:
    #                 if child.dep_ in ["nsubj", "agent"]:  # 주어 또는 agent
    #                     a0_info.append((child.idx, child.idx + len(child.text) - 1))
    #
    #             # A1 (Patient): 동사의 직접 객체
    #             for child in token.children:
    #                 if child.dep_ in ["dobj", "attr", "pobj"]:  # 직접 객체 또는 속성
    #                     a1_info.append((child.idx, child.idx + len(child.text) - 1))
    #
    #             a0_info_list.append(a0_info)
    #             a1_info_list.append(a1_info)
    #
    #             # VerbA0A1 (동사, Arg0, Arg1 관계)
    #             verb_a0a1_info_list.append([verb_info, a0_info, a1_info])
    #
    #     # DataFrame 형식으로 반환
    #     df = pd.DataFrame({
    #         "verb": verb_info_list,
    #         "A0": a0_info_list,
    #         "A1": a1_info_list,
    #         "verbA0A1": verb_a0a1_info_list  # A0 및 A1을 포함한 관계
    #     })
    #     return df
