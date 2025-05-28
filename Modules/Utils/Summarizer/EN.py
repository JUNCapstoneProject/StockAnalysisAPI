from torch.utils.data import Dataset
from transformers import pipeline
from datetime import datetime


class ENSummarizer:
    MODEL = 'facebook/bart-large-cnn'

    def __init__(self):
        self.summarizer = pipeline('summarization', model=self.MODEL)

    def summarize(self, text):
        outs = []  # outs 리스트를 while 루프 외부에서 선언

        while len(text) > 1024:
            chunk_text = self.get_overlapped_chunks(text, 1024, 64)
            for out in self.summarizer(ListDataset(chunk_text),
                                       batch_size=4, max_length=128, min_length=32):
                outs.append(out[0]['summary_text'])
            text = '\n'.join(outs)  # 새로 생성된 'outs'로 다시 text를 업데이트

        # 최종 요약 텍스트 생성
        summarized_text = self.summarizer('\n'.join(outs), max_length=128, min_length=32)[0]['summary_text']
        return summarized_text

    @staticmethod
    def get_overlapped_chunks(text, chunk, overlap):
        return [text[a:a + chunk] for a in range(0, len(text), chunk - overlap)]


class ListDataset(Dataset):
    def __init__(self, dataset):
        self.dataset = dataset

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, i):
        return self.dataset[i]
