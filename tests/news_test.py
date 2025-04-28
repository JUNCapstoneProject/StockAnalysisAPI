import json
import unittest
# bridge
from Modules.Utils.Interfaces.Pipeline import Input
from Modules.Utils.Summarizer.EN import ENSummarizer
from Modules.Utils.Translator.EN import ENTranslater
# FinReport
from Modules.AIAnalysis.Papers.FinReport.Adapter import adapter
from Modules.AIAnalysis.Papers.FinReport.NewsFactorization import NewsFactorInput
# NewsFactorization
from Modules.AIAnalysis.Papers.FinReport.NewsFactorization.Tokenizer import NewsTokenizer
from Modules.AIAnalysis.Papers.FinReport.NewsFactorization.SRL import TokenSRL
from Modules.AIAnalysis.Papers.FinReport.NewsFactorization.StockFactor import IntrinsicFactor
from Modules.AIAnalysis.Papers.FinReport.NewsFactorization.Classifier import SentimentClassifier
# TEST
from tests.DummyData.News.Yahoo import *
import mlflow.tensorflow


@adapter
def dummy_adapter(self, data):
    return data


class NewsTest(unittest.TestCase):
    pass
    # Success
    # def test_message(self):
    #     self.assertTrue(get_item())
    #     self.assertTrue(get_message())
    #     print('success test_message')

    # def test_load(self):
    #     ml_client = CLI.ml_client()
    #     mlflow.torch.load_model()

    # fail
    # def test_sentiment_classifier(self):
    #     self.en_summarizer = ENSummarizer()
    #     self.en_translater = ENTranslater()
    #     self.srl = TokenSRL()
    #     self.classifier = SentimentClassifier(self.srl.tokenizer)  # SRL과 동일한 tokenizer 사용
    #
    #     test_message = get_message()
    #     item = test_message['body']['item']
    #     data = dummy_adapter('dummy', item['data'])
    #     news_en = data['news_data']
    #     news_summarized = self.en_summarizer.summarize(news_en)
    #     self.assertTrue(news_summarized)
    #     news_cn = self.en_translater.to_cn(news_summarized)
    #     self.assertTrue(news_cn)
    #     news_factors = self.srl.labeling(news_cn)
    #     # self.assertFalse(news_factors.empty)  # 현재 df가 아니라 dict 사용중
    #     # create stock factor
    #     stock_factors = IntrinsicFactor.create_factor(data['stock_history'],
    #                                                   data['market_history'])
    #     self.assertTrue(len(stock_factors) > 0)
    #     # create sentiment factor
    #     input_data = {
    #         'text_a': [news_cn],
    #         'stock_factors': [stock_factors],
    #         'verb_mask': [news_factors['verb_mask'][0].tolist()],
    #         'A0_mask': [news_factors['A0_mask'][0].tolist()],
    #         'A1_mask': [news_factors['A1_mask'][0].tolist()],
    #         'AV_num': [news_factors['AV_num'][0].tolist()]
    #     }
    #     input_df = pd.DataFrame(input_data)
    #     sentiment_factor = self.classifier.classification(input_df)
    #     print(sentiment_factor)
    #     self.assertTrue(sentiment_factor)

    # Success
    # def test_socket(self):
    #     test_message = get_message()
    #     item = test_message['body']['item']
    #     data = item['data']
    #     data = dummy_adapter('dummy', data)
    #
    #     news_input = NewsFactorInput()
    #     sentiment_factor = news_input(data)
    #     print(sentiment_factor)
    #     self.assertTrue(sentiment_factor)


if __name__ == "__main__":
    unittest.main()
