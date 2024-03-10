from django.shortcuts import render
import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
import torch.nn.functional as F
#import numpy as np

# Instantiates the device to be used as GPU/CPU based on availability
device_gpu = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

MAX_OUTPUT_CHARS=30

eng_alphabets = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' # Defined no. of English letters in uppercase only
pad_char = ' ' # special character which may be used for denoting whitespace

# Assigning indexes to every 26 letters mentioned above
eng_alpha2index = {pad_char: 0} # let pad_char be at the o-th index
for index, alpha in enumerate(eng_alphabets):
    eng_alpha2index[alpha] = index+1

# Defined no. of Hindi letters = 128
hindi_alphabets = [chr(alpha) for alpha in range(2304, 2432)]
hindi_alphabet_size = len(hindi_alphabets)

hindi_alpha2index = {pad_char: 0}
for index, alpha in enumerate(hindi_alphabets):
    hindi_alpha2index[alpha] = index+1

# one-hot encoding
def word_rep(word, letter2index, device = device_gpu, pad_char=' '):
    rep = torch.zeros(len(word) + 1, 1, len(letter2index)).to(device)
    for letter_index, letter in enumerate(word):
        pos = letter2index.get(letter, letter2index.get(pad_char, 0))  # Use 0 as the default index
        rep[letter_index][0][pos] = 1
    pad_pos = letter2index.get(pad_char, 0)  # Use 0 as the default index for pad_char
    rep[len(word)][0][pad_pos] = 1  # Set the last position as the pad character
    return rep



# gt : ground truth (means hindi words)
def gt_rep(word, letter2index, device = device_gpu):
    gt_rep = torch.zeros([len(word)+1, 1], dtype=torch.long).to(device)
    for letter_index, letter in enumerate(word):
        pos = letter2index[letter]
        gt_rep[letter_index][0] = pos
    gt_rep[letter_index+1][0] = letter2index[pad_char]
    return gt_rep

def infer(net, word, max_output_chars, device=device_gpu):
  net.eval().to(device)
  word_ohe = word_rep(word, eng_alpha2index)
  output = net(word_ohe, max_output_chars)
  return output
# Create your views here.
def index(request):
    '''t_model = torch.load("Model/model.pth")
    t_model.eval()
    word = input("Enter the word :- ")
    print(word,len(word))
    w_list = word.split()
    print(w_list, len(w_list))

    for i in range(0, len(w_list)):
        out = infer(t_model, w_list[i].upper(), len(w_list[i])+1)
        for i in range(len(out)):
            print(list(hindi_alpha2index.keys())[list(hindi_alpha2index.values()).index(torch.argmax(out[i]))], end='')'''
    return render(request,'base.html')