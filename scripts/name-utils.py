#!/usr/bin/env python 

# Dylan W. Schwilk
# - editted by Will Pearse

# Utilities for matching taxon names, explaning from synonym lists, merging,
# and fuzzy matching using Levenshtein distances or ratios
# -- and now a little quicker using existing code
# 

import Levenshtein
from fuzzywuzzy import process
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

def find_fuzzy_match(pattern, x, threshold = 2, quick=False, max_return=20):
    """Return matches of items in x matching pattern at a threshold edit
    (?) distance. Setting 'quick' to true uses an additional
    cut-down step (because fuzzy searches are slow). 'max_return'
    sets the max. no. of hits to return (filter occurs *before*
    the threshold is applied). NOTE: because underlying code based
    on percentage match, there may be a (small) floating point
    effect.
    find_fuzzy_match("quercus robur", ["quercus ilex", "quercus robur"])
    """
    threshold = 100 - int(float(threshold) / len(pattern) * 100)
    if quick:
        x = difflib.get_close_matches(pattern, x)
    if len(x) > 0:
        best = process.extract(pattern, x, limit=max_return)
        return [x for x,y in best if y>threshold]

