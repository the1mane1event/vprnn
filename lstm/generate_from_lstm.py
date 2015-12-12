import sys
#sys.path.append('rnn-tutorial-rnnlm')
import csv
import itertools
import operator
import numpy as np
import nltk
import os
import time
import ast
from datetime import datetime
from utils import *
from lstm_theano import LSTMTheano



DATAFILE = "rnn-theano-100-82-2015-12-12-15-37-36.npz"
load_model_parameters_lstm('saved_model_parameters/{0}'.format(DATAFILE))
#MODEL = LSTMTheano(int(DATAFILE.split('-')[3]), hidden_dim=int(DATAFILE.split('-')[2]))
#load_model_parameters_lstm('../rnn-tutorial-rnnlm/data/{0}'.format(DATAFILE))


line_start_token = "LINE_START"
line_end_token = "LINE_END"
dictFile = 'dictFile.txt'
with open(dictFile) as f:
    dicts = []
    for line in f:
        line = ast.literal_eval(line)
        dicts.append(line)
char_to_code_dict, code_to_char_dict = dicts



def generate_sentence(model):
    # We start the sentence with the start token
    new_sentence = [char_to_code_dict[line_start_token]]
    # Repeat until we get an end token
    sampled_letter = None
    while sampled_letter != char_to_code_dict[line_end_token]:
        next_char_probs = model.forward_propagation(new_sentence)
        
        samples = np.random.multinomial(1, next_char_probs[-1])
        sampled_letter = np.argmax(samples)

        try:
            code_to_char_dict[sampled_letter]
        except:
            continue

        new_sentence.append(sampled_letter)
    sentence_str = [code_to_char_dict[x] for x in new_sentence[1:-1]]
    return sentence_str

num_sentences = 5
 
for i in range(num_sentences):
    sent = []
    sent = generate_sentence(MODEL)
    print "".join(sent)