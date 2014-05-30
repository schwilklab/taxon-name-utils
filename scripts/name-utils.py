#!/usr/bin/env python 

# Dylan W. Schwilk 

# Utilities for matching taxon names, explaning from synonym lists, merging,
# and fuzzy matching using Levenshtein distances or ratios
# 

import Levenshtein
#import pandas as pd
#t = pd.read_csv()

def agrepl(pattern, x, threshold = 2):
    """Return boolean vector of length x indicating items in x matching pattern at a
     threshold levenshtein distance"""
    return(map(lambda x : Levenshtein.distance(s,x) <= threshold, l))

def agrep(pattern, x, threshold = 2):
    """Return indices of items in x matching pattern at a
     threshold levenshtein distance"""
    from itertools import izip as zip, count # izip for maximum efficiency
    return([i for i, j in zip(count(), x) if Levenshtein.distance(pattern,j) <= threshold])
