from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import torch


def create_data_loader(df, tokenizer, max_len, batch_size):
    ds = GPReviewDataset(
        reviews=df.text_a.to_numpy(),
        targets=None,
        stock_factors=df.stock_factors,
        verb=df.verb_mask,
        A0=df.A0_mask,
        A1=df.A1_mask,
        AV_num=df.AV_num,
        tokenizer=tokenizer,
        max_len=max_len
    )

    return DataLoader(
        ds,
        batch_size=batch_size,
        # num_workers=4,
        shuffle=True
    )


class GPReviewDataset(Dataset):
    def __init__(self, reviews, targets, verb, A0, A1, AV_num, tokenizer, stock_factors, max_len):
        self.reviews = reviews
        self.targets = targets
        self.stock_factors = stock_factors
        self.verb = verb
        self.A0 = A0
        self.A1 = A1
        self.AV_num = AV_num
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.reviews)

    def __getitem__(self, item):
        review = str(self.reviews[item])
        target = self.targets[item]
        stock_factors = self.stock_factors[item]
        v = self.verb[item]
        a0 = self.A0[item]
        a1 = self.A1[item]
        av_num = self.AV_num[item]

        encoding = self.tokenizer.encode_plus(
            review,
            add_special_tokens=True,
            max_length=self.max_len,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )

        return {
            'review_text': review,
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'targets': torch.tensor(target, dtype=torch.long),
            'stock_factors': torch.tensor(stock_factors),
            'verb': torch.tensor(v),
            'A0': torch.tensor(a0),
            'A1': torch.tensor(a1),
            'AV_num': torch.tensor(av_num)
        }