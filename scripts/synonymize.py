#!/usr/bin/env python

"""This utility creates a synonym table from The Plant List data.

Allows expansion of a names list to a larger list including those names and all
synonyms. The merge action allows merging to a canonical list of names (not
necessarily TPL accepted names, although that is the default).

See the usage for more information.

This could be speeded up by cacheing the lookup dictionaries; as it works now,
the entire lookup data is re-read each time the program is run. But it works.

"""

__version__ =    '''0.2'''
__program__ =    '''synonymize.py'''
__author__  =    '''Dylan Schwilk'''
__usage__   =    '''synonymize.py [options] names_file'''

import codecs
import logging
logging.basicConfig(format='%(levelname)s: %(message)s')
tpl_logger = logging.getLogger('tpl_logger')

# The Plant List synonymy table:
TPL_FILE = "../data/theplantlist1.1/TPL1_1_synonymy_list"

# global dicts
syn2accepted = {}
accepted2syn = {}
tpl_accepted_names = []

def read_names(src):
    """`src` is a file object)"""
    return([line.rstrip() for line in src])

def make_tpl_dicts(tpl):
    """Create dictionaries from the tpl ragged array. `tpl` is a file object. There
can be multiple accepteds per synonym (synonyms without author info) and of
course multiple synonyms per accepted, so both dictionaries must be string:set

    """
    syn2accepted.clear()
    accepted2syn.clear()  
    for line in tpl:
        names = line[:-1].replace("_"," ").split(",")  # replace underscores with spaces
        syns = set(names)
        a = names[0]
        tpl_accepted_names.append(a)  # only used as a default canonical list for merging
        accepted2syn[a] = syns
        for n in syns :
            if syn2accepted.has_key(n) :
               syn2accepted[n].add(a)
            else :
                syn2accepted[n] = set([a])
            
def all_synonyms(name):
    """Find all synonyms traversing back through multiple accepteds if they exist.
This lumps together all synonyms with same name but different authors, but that
makese sense, I think. In other words. if name is a synonym of two different
accepteds,"A1" and "A2", then this function returns the full set of synonyms
for both those accepteds."""
    r =set()
    if syn2accepted.has_key(name): # is it even in TPL?
        for a in syn2accepted[name] :
            r.update(accepted2syn[a])
    return(r)

def expand_names(names):
    r = set()
    for name in names:
        r.add(name) # add itself
        r.update(all_synonyms(name))
    return(r)

def merge_names(badnames, goodnames=tpl_accepted_names):
    """Merge list of names using list or set "goodnames" as canonical names.
    Modifies badnames, but with synonyms replaced. If synonym not found, use
    actual name in badnames.

    """
    g = set(goodnames)
    for i,n in enumerate(badnames):
        if not n in g :  # name is not already canonical
            # 2 possibilities: it is an accepted name or a synonym
            accepteds = syn2accepted[n]
            cnames = accepteds.intersection(g)
            if len(cnames) > 0 : # accepts include canonical(s), pop one
                badnames[i] = cnames.pop()
            else : # last try; maybe there is a canonical sister synonym
                syns = all_synonyms(n) # get all sister syns of a
                snames = syns.intersection(g)
                if len(snames) > 0 :  # might was well take first one, no way to choose:
                    badnames[i] = snames.pop()
                # if this doesn't work, stick with original
                else :
                    tpl_logger.warning("Name not found: " + n)
    return

def main():
    '''Command line program.  '''
    import sys   
    from optparse import OptionParser

    # make sure stdin and stdout is in unicode
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    
    parser = OptionParser(usage=__usage__, version ="%prog " + __version__)
    parser.add_option("-a", "--action", action="store", type="string", \
                      dest="action",  default = 'expand', help="Action to perform, 'expand' or 'merge'")
    parser.add_option("-c", "--canonicalfile", action="store", type="string", dest="CANONICAL_NAMES_FILE", 
                       default="", help="file name for canonical names list, default is to use TPL accepted names")
    parser.add_option("-f", "--tplfile", action="store", type="string", dest="TPL_FILE", 
                      default=TPL_FILE, help="Set path to TPL ragged array, default=%default")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False,
                      help="Print INFO messages to stdout, default=%default")    

    (options, args) = parser.parse_args()

    if options.verbose:
        tpl_logger.setLevel(logging.INFO)
    
    if len(args) == 1 :
        try :
            names = read_names(codecs.open(args[0], "r", "utf-8"))
        except IOError:
            tpl_logger.error('Error reading file, %s' % args[0])
            sys.exit()
    else:
        # We can't use stdin as a fallback because we are not guaranteed stdin
        # to be utf on all platforms (python 3 fixes this)
        tpl_logger.error('No names file provided')
        sys.exit()

    # make the lookup. Note that PL lacks non ascii chars, but for internal
    # consistency, let's keep everything unicode
    make_tpl_dicts(codecs.open(options.TPL_FILE, "r", "utf-8"))

    # expand or merge
    if options.action=="expand" :
        r = expand_names(names)
    elif options.action=="merge":
        if options.CANONICAL_NAMES_FILE :
            canonical = read_names(open(options.CANONICAL_NAMES_FILE))
            merge_names(names, canonical)
        else :
            merge_names(names)
        r = names
    else :
        tpl_logger.error('Invalid action, %s' % options.action)
        sys.exit()

    # standard output only? should I make an file out option? Probably.
    for l in r:
        print(l)

    return(0)

if __name__== "__main__":
    main()
