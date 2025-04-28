from transformers import BertTokenizer, AutoModelForTokenClassification
import pandas as pd
import torch
import os

file_path = os.path.abspath(__file__)
directory = os.path.dirname(file_path)


class NewsTokenizer:
    TOKENIZER_DIR = os.path.join(directory, '../../../Models/ROBERT_4_model.bin')
    TOKENIZER_DIR = os.path.normpath(TOKENIZER_DIR)

    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained(self.TOKENIZER_DIR, do_lower_case=True)

    def tokenization(self, news_data):
        tokens = self.tokenizer.tokenize(news_data)
        return tokens
