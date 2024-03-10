#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import torch.nn as nn
import torch
import torch.optim as optim
from torch.autograd import Variable
import torch.nn.functional as F

MAX_OUTPUT_CHARS=30
device_gpu = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
class Transliteration_EncoderDecoder_Attention(nn.Module):

    def __init__(self, input_size, hidden_size, extra_layer_size, output_size, verbose=False):
        super(Transliteration_EncoderDecoder_Attention, self).__init__()

        self.hidden_size = hidden_size
        self.output_size = output_size

        self.encoder_rnn_cell = nn.GRU(input_size, hidden_size)
        self.decoder_rnn_cell = nn.GRU(hidden_size*2, hidden_size)

        self.h2o = nn.Linear(hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=2)

        self.U = nn.Linear(self.hidden_size, self.hidden_size)
        self.W = nn.Linear(self.hidden_size, self.hidden_size)
        self.attn = nn.Linear(self.hidden_size, 1)
        self.out2hidden = nn.Linear(self.output_size, self.hidden_size)
        # Extra layer after attention
        self.extra_layer_att = nn.Linear(self.hidden_size, extra_layer_size)

        self.verbose = verbose

    def forward(self, input, max_output_chars = MAX_OUTPUT_CHARS, device = device_gpu, ground_truth = None):

        # Defining the encoder
        encoder_outputs, hidden = self.encoder_rnn_cell(input)
        encoder_outputs = encoder_outputs.view(-1, self.hidden_size)

        if self.verbose:
            print('\n', 'Encoder output', encoder_outputs.shape)

        # Defining the decoder
        decoder_state = hidden
        decoder_input = torch.zeros(1, 1, self.output_size).to(device)

        outputs = []
        U = self.U(encoder_outputs)

        if self.verbose:
            print('\n', 'Decoder state', decoder_state.shape)
            print('\n', 'Decoder intermediate input', decoder_input.shape)
            print('\n', 'U * Encoder output', U.shape)

        for i in range(max_output_chars):

            W = self.W(decoder_state.view(1, -1).repeat(encoder_outputs.shape[0], 1))
            V = self.attn(torch.tanh(U + W))
            attn_weights = F.softmax(V.view(1, -1), dim = 1)

            if self.verbose:
                print('\n', 'W * Decoder state', W.shape)
                print('\n', 'V', V.shape)
                print('\n', 'Attn', attn_weights.shape)

            attn_applied = torch.bmm(attn_weights.unsqueeze(0),
                                 encoder_outputs.unsqueeze(0))

            # Applying extra layer after attention
            attn_applied = self.extra_layer_att(attn_applied)

            embedding = self.out2hidden(decoder_input)
            decoder_input = torch.cat((embedding[0], attn_applied[0]), 1).unsqueeze(0)

            if self.verbose:
                print('\n', 'Attn LC', attn_applied.shape)
                print('\n', 'Decoder input', decoder_input.shape)

            out, decoder_state = self.decoder_rnn_cell(decoder_input, decoder_state)

            if self.verbose:
                print('\n', 'Decoder intermediate output', out.shape)

            out = self.h2o(decoder_state)
            out = self.softmax(out)
            outputs.append(out.view(1, -1))

            if self.verbose:
                print('\n', 'Decoder output', out.shape)
                self.verbose = False

            max_idx = torch.argmax(out, 2, keepdim=True)
            if not ground_truth is None:
                max_idx = ground_truth[i].reshape(1, 1, 1)
            one_hot = torch.zeros(out.shape, device=device)
            one_hot.scatter_(2, max_idx, 1)

            decoder_input = one_hot.detach()

        return outputs



def main():
    """Run administrative tasks."""
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "IntelligentTransliteration.settings"
    )
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
