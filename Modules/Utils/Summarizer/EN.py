from transformers import pipeline


class ENSummarizer:
    MODEL = 'facebook/bart-large-cnn'

    def __init__(self):
        self.summarizer = pipeline('summarization', model=self.MODEL)

    def summarize(self, text):
        outs = []

        while len(text) > 1024:
            chunk_text = self.get_overlapped_chunks(text, 1024, 64)  # 이미 List[str] 형태여야 함
            for out in self.summarizer(chunk_text,
                                       max_length=128, min_length=32):
                outs.append(out['summary_text'])  # 'out'은 dict
            text = '\n'.join(outs)

        # 최종 요약
        summarized_text = self.summarizer(text, max_length=128, min_length=16)[0]['summary_text']
        return summarized_text

    @staticmethod
    def get_overlapped_chunks(text, chunk, overlap):
        return [text[a:a + chunk] for a in range(0, len(text), chunk - overlap)]
