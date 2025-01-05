#!/usr/bin/env python3

import glob
import re
import pandas as pd
import numpy as np

def get_conditions(blockcodes):
    r = re.compile(".*ID*")
    cond = list(filter(r.match, blockcodes))[0]
    if 'noID' in cond:
        ID = False
    else:
        ID = True
    if 'aud' in cond:
        feedback = 'A'
    else:
        feedback = 'O'
    return ID, feedback

def get_test_label(blockcode):
    if blockcode == 'test1':
        blockcode = 'pre'
    elif blockcode == 'test3':
        blockcode = 'post'
    else:
        blockcode = 'training'
    return blockcode

def get_words(stim_fp):
    stim = []
    for fp in stim_fp:
        fn = fp.split('\\')[2]
        stim.append(fn.split('.')[0])
    return stim

def check_answer(stim, responses):
    correct = []
    for answer, response in zip(stim, responses):
        if answer == response:
            correct.append(1)
        else:
            correct.append(0)
    return correct

training_scores = []
for file in glob.glob('../data/SLS*/*.dat'):
    print(f'Reading {file}')
    df = pd.read_csv(file, sep = '\t')

    # Extract some information
    blockcodes = list(np.unique(df.blockcode))
    sub = re.findall('SLS-(\d{1,4})', file)[0]
    ID, feedback = get_conditions(blockcodes)

    # Mark the training block
    training_df = df[df.blocknum == 2]
    training_df = training_df[training_df.trialcode == 'IDResponse']
    stim = get_words(training_df.stimulus2)
    correct = check_answer(stim, training_df.response)
    if len(training_df['trialcode']) != len(stim):
        print(f'Mismatching lengths for sub {sub}, skipping')
        continue
    training_df['trialcode'] = stim
    training_df['correct'] = correct
    test_label = 'training'
    
    # Score
    ncorrect = sum(training_df.correct)
    ntrials = max(training_df.trialnum)
    percent_correct = ncorrect/ntrials * 100

    block_scores = pd.DataFrame({
        'sub': [sub],
        'test': [test_label],
        'ID': [ID],
        'feedback': [feedback],
        'percent_correct': [percent_correct]
    })
    training_scores.append(block_scores)
    # break

pd.concat(training_scores)
scores = pd.concat(training_scores)
scores.to_csv('synthetic-speech-training-scores.csv', index = False)