import os
import pandas as pd
import torch
import cloudpickle
import torch.nn.functional as F
# brdige
from Modules.AIAnalysis.Papers.FinReport.NewsFactorization.SentimentClassifier.Model import SentimentClassifier as Model
from Modules.AIAnalysis.Papers.FinReport.NewsFactorization.SentimentClassifier.Dataset import create_data_loader

max_len = 300
BATCH_SIZE = 16
class_names = ['negative', 'neutral', 'positive']
file_path = os.path.abspath(__file__)
directory = os.path.dirname(file_path)


class SentimentClassifier:
    ENDPOINTS_URL = ''
    CLASSIFIER_DIR = os.path.join(directory, '../../../../Models/SentimentClassifier_/data/model.pth')
    CLASSIFIER_DIR = os.path.normpath(CLASSIFIER_DIR)

    def __init__(self, tokenizer):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.tokenizer = tokenizer
        self.model = Model(len(class_names), self.device)

    def classification(self, df: pd.DataFrame):
        data_loader = create_data_loader(df, self.tokenizer, max_len, BATCH_SIZE)
        y_review_texts, y_pred, y_pred_probs, y_test = self._get_predictions(data_loader)
        print(y_review_texts, y_pred, y_pred_probs, y_test)  # FIXME : TEST CODE
        return y_pred

    def _get_predictions(self, data_loader):
        self.model.load_state_dict(torch.load(self.CLASSIFIER_DIR, weights_only=False))
        self.model = self.model.to(self.device)
        self.model.eval()

        review_texts = []
        predictions = []
        prediction_probs = []
        real_values = []

        with torch.no_grad():
            for d in data_loader:
                texts = d["review_text"]
                input_ids = d["input_ids"].to(self.device)
                attention_mask = d["attention_mask"].to(self.device)
                targets = d["targets"].to(self.device)
                verb = d["verb"].to(self.device)
                stock_factors = d['stock_factors'].to(self.device)
                A0 = d["A0"].to(self.device)
                A1 = d["A1"].to(self.device)
                AV_num = d['AV_num'].to(self.device)

                outputs = self.model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    verb=verb,
                    A0=A0,
                    A1=A1,
                    stock_factors=stock_factors,
                    AV_num=AV_num
                )
                _, preds = torch.max(outputs, dim=1)

                probs = F.softmax(outputs, dim=1)

                review_texts.extend(texts)
                predictions.extend(preds)
                prediction_probs.extend(probs)
                real_values.extend(targets)

        predictions = torch.stack(predictions).cpu()
        prediction_probs = torch.stack(prediction_probs).cpu()
        real_values = torch.stack(real_values).cpu()
        return review_texts, predictions, prediction_probs, real_values
