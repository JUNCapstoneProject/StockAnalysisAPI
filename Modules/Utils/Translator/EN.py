from transformers import MarianMTModel, MarianTokenizer

model_name = "Helsinki-NLP/opus-mt-en-zh"
en_tokenizer = MarianTokenizer.from_pretrained(model_name)
model_to_cn = MarianMTModel.from_pretrained(model_name)


class ENTranslater:
    def __init__(self):
        self.en_tokenizer = en_tokenizer
        self.model_to_cn = model_to_cn

    def to_cn(self, en_text):
        translated = self.model_to_cn.generate(**en_tokenizer(en_text, return_tensors="pt", padding=True))
        return en_tokenizer.decode(translated[0], skip_special_tokens=True)
