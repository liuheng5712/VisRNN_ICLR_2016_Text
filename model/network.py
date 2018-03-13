import torch
import torch.nn as nn
from torch.autograd import Variable

import sys

import pdb

class CharRNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, model = "lstm", n_layers = 1):
        super(CharRNN, self).__init__()

        self.model = model.lower()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.n_layers = n_layers

        if self.model == "rnn":
            self.rnn = nn.RNN(input_size, hidden_size, n_layers, batch_first = True)
        elif self.model == "lstm":
            self.rnn = nn.LSTM(input_size, hidden_size, n_layers, batch_first = True)
        elif self.model == "gru":
            self.rnn = nn.GRU(input_size, hidden_size, n_layers, batch_first = True)
        else:
            raise Exception('No such a model! Exit.')
            sys.exit(-1)

        self.proj = nn.Linear(hidden_size, output_size)

    def forward(self, input, init_hidden):
        output, hidden = self.rnn(input, init_hidden)   # input: (batch, seq_len, input_size)
        decoded = self.proj(output) # output: (batch, seq_length, hidden_size * num_directions)

        return decoded, hidden  # decoded: (batch, seq_len, output_size)

    def init_hidden(self, batch_size):
        if self.model == "lstm":
            return (Variable(torch.zeros(self.n_layers, batch_size, self.hidden_size)),
                    Variable(torch.zeros(self.n_layers, batch_size, self.hidden_size)))

        return Variable(torch.zeros(self.n_layers, batch_size, self.hidden_size))

