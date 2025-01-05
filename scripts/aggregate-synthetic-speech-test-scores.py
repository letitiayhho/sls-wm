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

def get_test_label(blocknum):
    if blocknum == 1:
        block = 'pre'
    elif blocknum == 3:
        block = 'post'
    else:
        block = 'training'
    return block

scores = []
for file in glob.glob('../data/SLS*/*.dat'):
    print(f'Reading {file}')
    df = pd.read_csv(file, sep = '\t')

    # Extract some information
    blocknums = list(np.unique(df.blocknum))
    blockcodes = list(np.unique(df.blockcode))
    sub = re.findall('SLS-(\d{1,4})', file)[0]
    ID, feedback = get_conditions(blockcodes)
    
    # For each block number calculate percentage correct
    for blocknum in blocknums:
        test_label = get_test_label(blocknum)
        if test_label == 'training':
            continue

        ncorrect = sum(df.correct[df.blocknum == blocknum])
        ntrials = max(df.trialnum[df.blocknum == blocknum])
        percent_correct = ncorrect/ntrials * 100

        block_scores = pd.DataFrame({
            'sub': [sub],
            'test': [test_label],
            'ID': [ID],
            'feedback': [feedback],
            'percent_correct': [percent_correct]
        })
        scores.append(block_scores)
        # break
    # break

scores = pd.concat(scores)
scores
scores.to_csv('synthetic-speech-test-scores.csv', index = False)