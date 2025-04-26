import unittest
# LSTM
from Modules.Utils.Socket.Server import TCPSocketServer
from API.Controller.Analysis.Finance import FinanceAnalysisController
from API.Controller.Analysis.News import NewsAnalysisController
# TEST
# from tests.DummyData.Finance.Chart import *
from tests.DummyData.News.Yahoo import *


class SocketTest(unittest.TestCase):
    pass
    # Success
    # def test_message(self):
    #     self.assertTrue(get_item())
    #     self.assertTrue(get_message())
    #     print('success test_message')

    # TODO : Service.Finance 메모이자이즈 비활성화
    # Success
    # def test_finance_socket(self):
    #     FinanceAnalysisController()  # 등록
    #     path = '/finance/lstm'
    #     test_message = get_message()
    #     item = test_message['body']['item']
    #     message = TCPSocketServer.handle_request(path, item)
    #     print(message)

    def test_news_socket(self):
        NewsAnalysisController()  # 등록
        news_path = '/news/sentiment_classifier'
        test_message = get_message()
        item = test_message['body']['item']
        message = TCPSocketServer.handle_request(news_path, item)
        print(message)


if __name__ == "__main__":
    unittest.main()
