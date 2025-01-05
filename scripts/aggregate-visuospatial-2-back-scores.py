#!/usr/bin/env python3

import csv
import glob
import numpy as np
import pandas as pd
import re
from scipy.stats import norm

def score(fp):
    hits = 0
    misses = 0
    fas = 0
    holds = 0
    n_targets = 0
    n_noise = 0

    with open(fp, mode = 'r') as file:
        reader = csv.reader(file)
        next(reader, None) # Skip the header row 

        for row in reader: 
            trial_type = row[11]
            target = row[14]
            
            if trial_type == 'n-back-trial' and target != 'FIRSTS':  
                responded = int(row[12])
                # print(f'trial_type: {trial_type}, responded: {responded}, target: {target}')

                if target == 'T':
                    n_targets +=1 
                    if responded:
                        hits +=1
                    else:
                        misses +=1
                
                if target == 'NT':
                    n_noise += 1
                    if responded:
                        fas +=1
                    else:
                        holds += 1

#    print(hits)
#    print(n_targets)
#    print(fas)
#    print(n_noise)
    hit_rate = hits / n_targets
    fa_rate = fas / n_noise

    # if someone gets perfect score, either hit rate of 1 or false alarm rate of 0
    if hit_rate == 1:
        hit_rate = ((hits * 2) - 1) / (n_targets * 2)
    if fa_rate == 0:
        fa_rate = 1/(2*n_noise)

    z_score_hit = norm.ppf(hit_rate)
    z_score_fa = norm.ppf(fa_rate)
    d_prime = z_score_hit - z_score_fa

    return hit_rate, fa_rate, d_prime


df = pd.DataFrame()
for fp in glob.glob('../data/SLS-*/Visuospatial*.csv'):
    print(fp)
    sub = re.findall('SLS-(\d{1,4})', fp)[0]

    hit_rate, fa_rate, d_prime = score(fp)
    sub_d = {
        'sub': [sub],
        'hit_rate': [hit_rate],
        'fa_rate': [fa_rate],
        'd_prime': [d_prime]
    }
    sub_df = pd.DataFrame(sub_d)
    df = pd.concat([df, sub_df], ignore_index = True)
print('Writing to visuospatial-2-back-scores.csv')
df.to_csv('visuospatial-2-back-scores.csv', index = False)