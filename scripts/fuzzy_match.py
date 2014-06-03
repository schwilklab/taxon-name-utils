#!/usr/bin/env python 

# Authors: Dylan W. Schwilk and Will Pearse

# Utilities for fuzzy matching taxon names
# 

from Levenshtein import jaro_winkler as jaro_winkler
#from jellyfish import jaro_winkler as jaro_winkler

import sys, logging
logging.basicConfig(format='%(levelname)s: %(message)s')
logger = logging.getLogger('tu_logger')

# two alternative levenshtein distance based matcher methods. Which is faster?
from automata import Matcher as Matcher  # use Levenshtein automaton and DFA
#import lev_trie.Matcher as tMatcher  # store all distances as Trie


THRESHOLD_DIST = 2  # First pass list up to 2 edits (uses levenshtein automata) 
THRESHOLD_JW = 0.96 # Final pass Jaro-Winkler cutoff for match

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

def best_jw_match(pattern, matches, jw_threshold=THRESHOLD_JW):
    """Find match within list of candidates with highest Jaro-Winkler similarity.
Return None if no match is higher than jw_threshold

    """
    jw_dists = map(lambda n : jaro_winkler(pattern,n), matches)
    max_jw = max(jw_dists)
    if(max_jw > jw_threshold) :
        bmatch = matches[jw_dists.index(max_jw)]
        return(bmatch)
    return(None)

def get_matches(pattern, matcher, limit=THRESHOLD_DIST):
    """Return all matches in Matcher object m limit distance or closer to pattern.
See automata.py

    """
    return(matcher.search(pattern, limit))

def best_match(pattern, m, limit=1):
    """Return best match to pattern in Matcher object, m. This is a two step
process: First all candidate matches are found up to limit edits from pattern.
Then the candidate with the highest Jaro-Winkler similarity (default weighting)
is chosen."""
    if(pattern == m(pattern)) : return pattern  # first check for exact match!
    matches = get_matches(pattern, m)
    if(matches):
        return(best_jw_match(pattern, matches))
    return(None)

def fuzzy_match_name_list(dlist, elist, outfile=sys.stdout):
    """Match all taxon names in dlist to best match in elist. Return dictionary
with matchable names in dlist as keys and best match in elist as values. The
function writes the output as it progresses so that state is saved (slow
process), default output is stdout.

    """

    res = {}
    ## Get genus->species dicts for both lists
    enames = genus_species(elist)
    egenera = enames.keys()
    egenera.sort()

    dnames = genus_species(dlist)

    genus_matcher = Matcher(egenera, True)
    count=0
    for genus in sorted(dnames.keys()) :
        best_genus = best_match(genus, genus_matcher)
        if best_genus :
            se_matcher = Matcher(sorted(enames[best_genus]), True)
            for se in dnames[genus]:
                if count % 100 == 0 : logger.info(str(count) + ": " + genus)
                count = count+1
                best_se = best_match(se, se_matcher)
                if best_se :
                    # add name to list of matches to "best_match"
                    bname = best_genus + " " + best_se
                    name = genus + " " + se
                    res[name] = bname
                    outfile.write(name + "," + bname + "\n")
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
