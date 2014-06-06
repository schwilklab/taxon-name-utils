#!/usr/bin/env python 

# Authors: Dylan W. Schwilk and Will Pearse

# Utilities for fuzzy matching taxon names

from Levenshtein import jaro_winkler as jaro_winkler
import re

import sys, logging
logging.basicConfig(format='%(levelname)s: %(message)s')
logger = logging.getLogger('tu_logger')

# two alternative levenshtein distance based matcher methods. Which is faster?
from automata import Matcher as Matcher  # use Levenshtein automaton and DFA
#import lev_trie.Matcher as tMatcher  # store all distances as Trie


# DEFAULTS:
THRESHOLD_DIST_GENUS = 2 # edit distance
THRESHOLD_DIST_SE = 3
THRESHOLD_JW = 0.94 # Final pass Jaro-Winkler cutoff for match

def is_gender_switch(seA, seB):
    """Check if specific epithet difference is simply one of latin gender."""
    # constants
    m  = re.compile(r"(^.+?)(r|re|us|um|er|rum|a|ra|ris|rus|iae|ae|ensis|ense|ii|i)$")
    gender_eq = { "us" : set(["a", "um"]) , 
                  "um" : set(["a", "us"]),
                  "er" : set(["ra", "rum"]),
                  "rum": set(["ra", "er"]),
                  "r"  : set(["ris", "re"]),
                  "re" : set(["ris", "r"]),
                  "a"  : set(["us", "um"]),
                  "ra" : set(["er", "rum"]),
                  "ris": set(["r", "re"]),
                  "ae" : set(["iae",]),
                  "iae": set(["ae",]),
                  "ense": set(["ensis",]),
                  "ensis": set(["ense",]),
                  "ii":  set(["i",]),
                  "i" : set(["ii",]),
                  "ra": set(["rus",]),
                  "rus": set(["ra",])}

    try :
        Aparts = re.match(m, seA)
        Bparts = re.match(m, seB)
        A1, A2 = Aparts.groups()
        B1, B2 = Bparts.groups()
  #      print(A1, A2, B1, B2)
  #      print(gender_eq[B2])
        if ((A1 == B1) and A2 in gender_eq[B2]) :
            return True
        else :
            return False
    except :
        return False


def genus_species(names):
    """Split names into genus and set of species. Return dictionary of strings to
sets."""
    genera = {}
    for name in names:
        parts = name.split()  # ignore all parts after
        genus = parts[0]
        se = parts[1]
        genera.setdefault(genus, set())
        genera[genus].add(se)

    return(genera)

def best_jw_match(pattern, matches, jw_threshold):
    """Find match within list of candidates with highest Jaro-Winkler similarity.
Return None if no match is higher than jw_threshold. Returns tuple (match, jw_similarity)"""
    jw_dists = map(lambda n : jaro_winkler(pattern,n), matches)
    max_jw = max(jw_dists)
    if(max_jw >= jw_threshold) :
        bmatch = matches[jw_dists.index(max_jw)]
        return((bmatch, max_jw))
    return((None,None))


def get_matches(pattern, matcher, limit):
    """Return all matches in Matcher object m limit distance or closer to pattern.
See automata.py"""
    return(matcher.search(pattern, limit))



def best_match(pattern, m, limit, jw_threshold):
    """Return best match to pattern in Matcher object, m. This is a two step
process: First all candidate matches are found up to limit edits from pattern.
Then the candidate with the highest Jaro-Winkler similarity (default weighting)
is chosen. Returns tuple (match, jw_similarity)."""
    if(pattern == m(pattern)) : return((pattern,1.0))  # first check for exact match!
    matches = get_matches(pattern, m, limit)
    if(matches):
        return(best_jw_match(pattern, matches, jw_threshold))
    return((None,None))


def fuzzy_match_name_list(dlist, elist, outfile=sys.stdout, genus_dist= THRESHOLD_DIST_GENUS, se_dist = THRESHOLD_DIST_SE, threshold_jw = THRESHOLD_JW):
    """Match all taxon names in dlist to best match in elist. Return dictionary
with matchable names in dlist as keys and best match in elist as values. The
function writes the output as it progresses so that state is saved (slow
process), default output is stdout.

    """

    ## Get genus->species dicts for both lists
    enames = genus_species(elist)
    egenera = enames.keys()
    egenera.sort()

    dnames = genus_species(dlist)

    res = {}
    genus_matcher = Matcher(egenera, True)
    count=0
    # write header
    outfile.write("dlist,elist,genus_jw,se_jw,gender_switch\n")
    for genus in sorted(dnames.keys()) :
        best_genus, genus_jw = best_match(genus, genus_matcher, genus_dist, threshold_jw)
        if best_genus :
            se_matcher = Matcher(sorted(enames[best_genus]), True)
            for se in dnames[genus]:
                if count % 100 == 0 : logger.info(str(count) + ": " + genus)
                count = count+1
                (best_se, jw) = best_match(se, se_matcher, se_dist, threshold_jw)
                if best_se :
                    # add name to list of matches to "best_match"
                    bname = best_genus + " " + best_se
                    name = genus + " " + se
                    res[name] = bname
                    if is_gender_switch(se, best_se) : gender_switch = "True"
                    else : gender_switch = "False"
                    outfile.write(name + "," + bname + "," + str(genus_jw) + "," + str(jw) + "," + gender_switch + "\n")

            # else :
            #     logger.info("Unmatched: " + genus + "\n")
        else:
            # logger.info("Unmatched: " + genus + "\n")
            if count % 100 == 0 : logger.info(str(count) + ": " + genus)
            count = count+1

    return(res)


def _time_fuzzy_matching():
    """Run timing tests on various fuzzy matching functions"""

    from timeit import Timer

    setup_auto="""
import codecs
import automata
from automata import Matcher as Matcher
from __main__ import fuzzy_match_name_list
gbifnames = [line.strip() for line in codecs.open("../data/name-lists/gbif-occurrences-names.txt", "r", "utf-8")]
tanknames = [line.strip() for line in codecs.open("../results/expanded-tank-tree-names.txt", "r", "utf-8")]
outf = codecs.open("../results/fuzzy_test_output.txt", "w", "utf-8")
"""

    setup_trie="""
import codecs
import lev_trie
from lev_trie import Matcher as Matcher
from __main__ import fuzzy_match_name_list
gbifnames = [line.strip() for line in codecs.open("../data/name-lists/gbif-occurrences-names.txt", "r", "utf-8")]
tanknames = [line.strip() for line in codecs.open("../results/expanded-tank-tree-names.txt", "r", "utf-8")]
outf = codecs.open("../results/fuzzy_test_output.txt", "w", "utf-8")
"""

    time_lev_automata = Timer("""fuzzy_match_name_list(gbifnames[0:700],tanknames, outf)""", setup_auto)
    time_lev_trie = Timer("""fuzzy_match_name_list(gbifnames[0:700],tanknames, outf)""", setup_trie)

    print("Using Levenshtein automata")
    print(time_lev_automata.timeit(number=1))
    print("Using Levenshtein and trie")
    print(time_lev_trie.timeit(number=1))

if __name__ == "__main__":
    # default script runs tests

    # TODO: write comamnd line version with options
    _time_fuzzy_matching()
