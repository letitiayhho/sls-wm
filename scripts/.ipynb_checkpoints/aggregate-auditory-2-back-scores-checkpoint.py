#!/usr/bin/env python3

import pandas as pd
from scipy.stats import norm
import glob
import re

# Extract scores
def score(df):    
    # Compute hit rate
    hits = int(df.HIT_2B[df.designation == 'ANB-SUMMARY'])
    targets = sum(df.TYPE == 'T')
    hit_rate = hits / targets
    
    # Compute false alarm rate
    fas = int(df.FA_2B[df.designation == 'ANB-SUMMARY'])
    not_targets = sum(df.TYPE == 'NT')
    fa_rate = fas / not_targets
    
    # Compute d'
    if hit_rate == 1:
        hit_rate = ((hits * 2) - 1) / (targets * 2)
    if fa_rate == 0:
        fa_rate = 1/(2*not_targets)

    zscore_hit = norm.ppf(hit_rate)
    zscore_fa = norm.ppf(fa_rate)
    d_prime = zscore_hit - zscore_fa

    # print(f'hit_rate: {hit_rate}')
    # print(fa_rate: {fa_rate}')
    # print(f'd_prime: {d_prime}')
    return(hit_rate, fa_rate, d_prime)

df = pd.DataFrame()
for fp in glob.glob('../data/SLS-*/Auditory*.csv'):
    print(fp)
    sub = re.findall('SLS-(\d{1,4})', fp)[0]
    
    sub_df = pd.read_csv(fp)
    hit_rate, fa_rate, d_prime = score(sub_df)
    sub_d = {
        'sub': [sub],
        'hit_rate': [hit_rate],
        'fa_rate': [fa_rate],
        'd_prime': [d_prime]
    }
    sub_df = pd.DataFrame(sub_d)
    df = pd.concat([df, sub_df], ignore_index = True)
print('Writing to auditory-2-back-scores.csv')
df.to_csv('auditory-2-back-scores.csv', index = False)