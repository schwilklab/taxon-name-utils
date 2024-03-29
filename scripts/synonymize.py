#!/usr/bin/env python

"""This utility creates a synonym table for a species list.

The original version used The Plant List. The current version uses the backbone
data download from World Flora Online.

Allows expansion of a names list to a larger list including those names and all
synonyms. The merge action allows merging to a canonical list of names (not
necessarily "accepted names", although that is the default).

See the usage for more information.

This could be speeded up by cacheing the lookup dictionaries; as it works now,
the entire lookup data is re-read each time the program is run. But it works.

"""

__version__ =    '''0.4'''
__program__ =    '''synonymize.py'''
__author__  =    '''Dylan Schwilk'''
__usage__   =    '''synonymize.py [options] names_file'''

import codecs
import logging
import os
logging.basicConfig(format='%(levelname)s: %(message)s')
syn_logger = logging.getLogger('tpl_logger')

# The Plant List synonymy table: currently with underscores separating name
# parts, hence need to replace with spaces in code below.

# SYN_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)),
#                         "../data/theplantlist1.1/TPL1_1_synonymy_list")

## WorldFlora online backbone data

SYN_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        "../data/WorldFlora/WFO_synonyms_list")

# global dicts
syn2accepted = {} # lookup accepted name for any name
accepted2syn = {} # get set of synonyms for an accepted name (includes accepted name itself)
accepted_names = set()
syn2canonical = {}  # for canonical names that may not equal synonym data "accepted names"
canonical_names = set()

def read_names(src):
    """`src` is a file object)"""
    return([line.rstrip() for line in src])

# def make_binom(name):
#     """Converts a possibly three or more part name to a simple binomial."""
#     l = name.split()
#     return(l[0] + " " + l[1])

def make_syn_dicts(synarray):
    """Create dictionaries from the synonym data ragged array. `synarray` is a file
object. There can be multiple accepteds per synonym (synonyms without author
info) and of course multiple synonyms per accepted, so both dictionaries must
be string:set

    """
    syn2accepted.clear()
    accepted2syn.clear()  
    for line in synarray:
        l = line.rstrip(",\n") # should change in WFO read
        names = l.split(",")
        syns = set(names)
        a = names[0]    # accepted name is first in list   
        accepted_names.add(a)  # only used as a default canonical list for merging
        accepted2syn[a] = syns
        for n in syns :
            if n in syn2accepted :
               syn2accepted[n].add(a)
            else :
                syn2accepted[n] = set([a])
            
def all_synonyms(name):
    """Find all synonyms traversing back through multiple accepteds if they exist.
If name is a synonym of two different accepteds,"A1" and "A2", then this
function returns the full set of synonyms for both those accepteds. Note if the
synonym database lacks authors, then this lumps together all synonyms with same
name but different authors. This means that in final name matching any synonym
that matches two or more accepteds will need to be checked separately. Flag
such cases in the matching code

    """
    r =set()
    if name in syn2accepted: # is it even in the data?
#        print(len(syn2accepted[name]))
#        print(name, syn2accepted[name])
        for a in syn2accepted[name] :
            r.update(accepted2syn[a])
#            print(accepted2syn[a])
    return(r)

def expand_names(names):
    r = set()
    for name in names:
        syns = all_synonyms(name)
        syns.add(name)
        canonical_names.add(name)
        for n in syns :
            syn2canonical[n] = name  ## this is the lookup table needed by bad2good. TODO: make set, allow multiple and check
        r.update(syns)
    return(r)

def bad2good(bad, strict=True):
    """Note: you must run expand_names first so that syn2canonical is filled.TODO:
add warning in case of multiple"""
    if bad in canonical_names: return bad # avoid overwriting in case of
                                          # non-unique merge
    if strict : default = ""
    else : default = bad
    return(syn2canonical.get(bad, default))

def merge_names(badnames, goodnames=accepted_names, strict=False):
    """Merge list of names using list or set "goodnames" as canonical names. If
    synonym not found, use actual name in badnames (strict=False)

    """
    g = set(goodnames)
    res = [""] * len(badnames)

    expand_names(g) # need to fill syn2canonical!
    for i,n in enumerate(badnames):
        res[i] = bad2good(n, strict=strict)
     #   if (i % 100 == 0) :
     #       print(res[i])
    return res

def main():
    '''Command line program.  '''
    import sys   
    from optparse import OptionParser

    # make sure stdin and stdout is in unicode
    #sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    sys.stdout.reconfigure(encoding='utf-8')
    
    parser = OptionParser(usage=__usage__, version ="%prog " + __version__)
    parser.add_option("-a", "--action", action="store", type="string",
                      dest="action",  default = 'expand',
                      help="Action to perform, 'expand' or 'merge'")
    parser.add_option("-c", "--canonicalfile", action="store", type="string",
                      dest="CANONICAL_NAMES_FILE",
                      default="", help="file name for canonical names list, default is to use synonym data accepted names")
    parser.add_option("-f", "--synfile", action="store", type="string", dest="SYN_FILE", 
                      default=SYN_FILE, help="Set path to synonym file ragged array, default=%default")
    # parser.add_option("-b", "--binomial", action="store_true",
    #                   dest="force_binomial", default=False,
    #                   help="Use only binomial species names and ignore infraspecific epithets, default=%default")    
    # parser.add_option("-s", "--scrub", action="store_true", dest="scrub_var", default=False,
    #                   help="Remove `var.` and `subsp.` from synonyms, default=%default")    
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False,
                      help="Print INFO messages to stdout, default=%default")    

    (options, args) = parser.parse_args()

    if options.verbose:
        syn_logger.setLevel(logging.INFO)
    
    if len(args) == 1 :
        try :
            names = read_names(codecs.open(args[0], "r", "utf-8"))
            # if options.force_binomial :
            #     names = map(make_binom, names)
        except IOError:
            syn_logger.error('Error reading file, %s' % args[0])
            sys.exit()
    else:
        # We can't use stdin as a fallback because we are not guaranteed stdin
        # to be utf on all platforms (python 3 fixes this)
        syn_logger.error('No names file provided')
        sys.exit()

    # make the lookup and keep everything unicode
    make_syn_dicts(codecs.open(options.SYN_FILE, "r", "utf-8"))

    # expand or merge
    if options.action=="expand" :
        r = expand_names(names)
    elif options.action=="merge":
        if options.CANONICAL_NAMES_FILE :
            canonical = read_names(codecs.open(options.CANONICAL_NAMES_FILE, "r", "utf-8"))
            r = merge_names(names, canonical)
        else :
            r = merge_names(names)
    else :
        syn_logger.error('Invalid action, %s' % options.action)
        sys.exit()

    # standard output only? should I make an file out option? Probably.
    for l in r:
        print(l)

    return(0)

if __name__== "__main__":
    main()
