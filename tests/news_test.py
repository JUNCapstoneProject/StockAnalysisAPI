import json
import unittest
import numpy as np
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
from Modules.AIAnalysis.Papers.FinReport.NewsFactorization.SentimentClassifier.Dataset import create_data_loader
# TEST
from tests.DummyData.News.Yahoo import *
from sklearn.metrics import confusion_matrix, classification_report
import ast


@adapter
def dummy_adapter(self, data):
    return data


def string_to_tuples_list(text):
    if text is np.nan or text == '[]':
        return []
    text = ''.join(text.split('], ['))
    tmp = eval(text.strip('[').strip(']'))
    if not isinstance(tmp[0], tuple):
        return [tmp]
    return list(tmp)


class NewsTest(unittest.TestCase):
    pass
    # Success
    # def test_message(self):
    #     # self.assertTrue(get_item())
    #     self.assertTrue(get_message())
    #     print('success test_message')

    # Success
    # def test_load(self):
    #     ml_client = CLI.ml_client()
    #     mlflow.torch.load_model()

    # Success
    # memoize=True 성공
    def test_sentiment_classifier(self):
        test_message = get_message()
        item = test_message['body']['item']
        data = item['data']

        news_input = NewsFactorInput(memoize=False)
        sentiment_factor = news_input(data)
        print(sentiment_factor)
        self.assertTrue(sentiment_factor)

    # def test_model(self):
    #     class_names = ['negative', 'neutral', 'positive']
    #
    #     df_test = pd.read_csv('DummyData/Finance/test.csv', sep='\t')
    #     for col in ['verb', 'A0', 'A1']:
    #         df_test[col] = df_test[col].apply(string_to_tuples_list)
    #
    #     for col in ['stock_factors', 'verbA0A1']:
    #         df_test[col] = df_test[col].apply(ast.literal_eval)
    #
    #     df_test = df_test.reset_index(drop=True)
    #     tokenizer = TokenSRL().tokenizer
    #     classifier = SentimentClassifier(tokenizer)
    #     y_review_texts, y_pred, y_pred_probs, y_test = classifier.test_classification(df_test)
    #     print(classification_report(y_test, y_pred, target_names=class_names, digits=4))


if __name__ == "__main__":
    unittest.main()
