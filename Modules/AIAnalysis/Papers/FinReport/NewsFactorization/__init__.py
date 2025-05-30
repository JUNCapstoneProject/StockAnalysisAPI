# bridge
import copy

import pandas as pd
from Modules.Utils.Interfaces.Pipeline import Input
from Modules.Utils.Summarizer.EN import ENSummarizer
from Modules.Utils.Translator.EN import ENTranslater
from API.Socket.Client import SocketClient
from Modules.Utils.Decorator import memoization
from Modules.AIAnalysis.Papers.FinReport.Adapter import adapter
# NewsFactorization
from API.Socket.Messages.request import news_item
from Modules.AIAnalysis.Papers.FinReport.NewsFactorization.Tokenizer import NewsTokenizer
from Modules.AIAnalysis.Papers.FinReport.NewsFactorization.SRL import TokenSRL
from Modules.AIAnalysis.Papers.FinReport.NewsFactorization.StockFactor import IntrinsicFactor
from Modules.AIAnalysis.Papers.FinReport.NewsFactorization.Classifier import SentimentClassifier


class NewsFactorInput(Input):
    def __init__(self, memoize):
        self.memoize = memoize
        self.module_name = 'sentiment_classifier'
        self.en_summarizer = ENSummarizer()
        self.en_translater = ENTranslater()
        self.srl = TokenSRL()
        self.classifier = SentimentClassifier(self.srl.tokenizer)  # SRL과 동일한 tokenizer 사용
        self.client = SocketClient()

    # def __call__(self, data):
    #     # create news factor
    #     news_en = data['news_data']
    #     news_summarized = self.en_summarizer.summarize(news_en)
    #     news_cn = self.en_translater.to_cn(news_summarized)
    #     news_factors = self.srl.labeling(news_cn)
    #     # create stock factor
    #     stock_factors = IntrinsicFactor.create_factor(data['stock_history'],
    #                                                   data['market_history'])
    #     # create sentiment factor
    #     input_df = pd.DataFrame({
    #         'news_factors': [news_factors],
    #         'stock_factors': [stock_factors]
    #     })
    #     sentiment_factor = self.classifier.classification(input_df)
    #     return sentiment_factor

    @memoization
    @adapter
    def __call__(self, data):
        if self.memoize:
            return
        else:
            # create news factor
            news_en = data['news_data']
            news_summarized = self.en_summarizer.summarize(news_en)
            news_cn = self.en_translater.to_cn(news_summarized)
            news_factors = self.srl.labeling(news_cn)
            # create stock factor
            stock_factors = IntrinsicFactor.create_factor(data['stock_history'],
                                                          data['market_history'])
            # create sentiment factor
            item = copy.deepcopy(news_item)
            item['event_type'] = 'news'
            item['data'] = {
                'text_a': [news_cn],
                'stock_factors': [stock_factors],
                'verb_mask': [news_factors['verb_mask'][0].tolist()],
                'A0_mask': [news_factors['A0_mask'][0].tolist()],
                'A1_mask': [news_factors['A1_mask'][0].tolist()],
                'AV_num': [news_factors['AV_num'][0].tolist()]
            }
            message = self.client.request_tcp(item)
            if message['status_code'] == 200:
                return message['item']['result']
            else:
                raise Exception(message['message'])
