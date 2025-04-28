import os
from torch import nn
import torch
from transformers import BertModel

file_path = os.path.abspath(__file__)
directory = os.path.dirname(file_path)

NUMBER_FACTOR = 24
BERT_DIR = os.path.join(directory, '../../../../Models/ROBERT_4_model.bin')
BERT_DIR = os.path.normpath(BERT_DIR)


class SentimentClassifier(nn.Module):
    def __init__(self, n_classes, device):
        super(SentimentClassifier, self).__init__()
        self.bert = BertModel.from_pretrained(BERT_DIR)
        self.device = device
        self.encoder_layer = nn.TransformerEncoderLayer(d_model=2304 + NUMBER_FACTOR, nhead=1)
        self.transformer_encoder = nn.TransformerEncoder(self.encoder_layer, num_layers=2)
        self.drop = nn.Dropout(p=0.1)
        # self.L1 = nn.Linear(self.bert.config.hidden_size*30, self.bert.config.hidden_size*3)
        self.out1 = nn.Linear((self.bert.config.hidden_size * 3 + NUMBER_FACTOR) * 10,
                              (self.bert.config.hidden_size * 3 + NUMBER_FACTOR) * 3)
        self.out = nn.Linear((self.bert.config.hidden_size * 3 + NUMBER_FACTOR) * 3, n_classes)
        self.linear_for_stock_factors = nn.Linear(NUMBER_FACTOR, NUMBER_FACTOR)
        self.flatten2 = nn.Flatten(2, -1)
        self.flatten = nn.Flatten(1, -1)
        self.relu = nn.ReLU()
        self.sig = nn.Sigmoid()
        self.Querry = nn.Linear(self.bert.config.hidden_size, self.bert.config.hidden_size)
        self.Key = nn.Linear(self.bert.config.hidden_size, self.bert.config.hidden_size)

    # Factor24_Pretrained_RoBert_SRL(FC).ipynb
    def forward(self, input_ids, attention_mask, verb, A0, A1, stock_factors, AV_num):
        # get bert embedding
        hidden_state = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )[0]
        batch = hidden_state.shape[0]
        verb_tmp = verb.clone()

        # stock_factor(8*24)
        stock_factors_batch = stock_factors[:, :NUMBER_FACTOR]
        stock_factors_batch = self.linear_for_stock_factors(stock_factors_batch.float())
        stock_factors_batch = self.relu(stock_factors_batch)
        stock_factors_batch = torch.unsqueeze(stock_factors_batch, 1)  # 8*1*2304
        stock_factors_batch = torch.cat(10 * [stock_factors_batch], 1)

        # mask verb
        for idx, num in enumerate(AV_num):
            stock_factors_batch[idx] = torch.cat(num * [torch.unsqueeze(stock_factors_batch[idx][0], 0)] +
                                                 (10 - num) * [torch.zeros((1, NUMBER_FACTOR)).to(self.device)])

        # get verb embedding after masking (8*10*1*768)
        print('verb.shape :', verb.shape)
        V_mask = torch.unsqueeze(verb, 3)
        V_mask = torch.cat(768 * [V_mask], 3)
        print('V_mask.shape :', V_mask.shape)
        print('hidden_state.shape :', hidden_state.shape)
        transformer_input = torch.mean(V_mask * torch.unsqueeze(hidden_state, 1), 2, True)

        # get A0 embedding (8*10*2*768)
        A0_mask = torch.unsqueeze(A0, 3)
        A0_mask = torch.cat(768 * [A0_mask], 3)
        A0_mask = torch.mean(A0_mask * torch.unsqueeze(hidden_state, 1), 2, True)
        transformer_input = torch.cat([transformer_input, A0_mask], 2)

        # get A1 embedding (8*10*3*768)
        A1_mask = torch.unsqueeze(A1, 3)
        A1_mask = torch.cat(768 * [A1_mask], 3)
        A1_mask = torch.mean(A1_mask * torch.unsqueeze(hidden_state, 1), 2, True)
        transformer_input = torch.cat([transformer_input, A1_mask], 2)

        # get transformer input (8*10*2304)
        transformer_input = self.flatten2(transformer_input.float())
        transformer_input = torch.cat([transformer_input, stock_factors_batch], 2)

        # turn to (11*8*2304)
        transformer_input = torch.stack([transformer_input[:, i, :] for i in range(0, len(verb[0]))])

        # get transformer output (11*8*2304)
        transformer_output = self.transformer_encoder(transformer_input)

        # turn to (8*11*2304)
        transformer_output = torch.stack([torch.squeeze(transformer_output[:, i, :]) for i in range(0, batch)])
        transformer_output = torch.squeeze(transformer_output)
        if transformer_output.dim() == 2:
            transformer_output = torch.unsqueeze(transformer_output, 0)

        output = self.flatten(transformer_output.float())
        output = self.sig(output)
        # output = self.drop(output)
        output = self.out1(output)
        output = self.sig(output)
        output = self.drop(output)
        output = self.out(output)

        return output