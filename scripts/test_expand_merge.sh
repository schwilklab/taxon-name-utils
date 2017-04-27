#!/usr/bin/env bash

CANONICAL_NAMES="../data/name-lists/tank-tree-names.txt"
EXPANDED_NAMES="../results/expanded-tank-tree-names.txt"

# proof this is reversible (uncomment to test):
# python synonymize.py -a expand $CANONICAL_NAMES > $EXPANDED_NAMES
# diff -s <(sort $CANONICAL_NAMES) <(python synonymize.py -a merge -c $CANONICAL_NAMES $EXPANDED_NAMES | sort | uniq)

# proof this is reversible with -b option (uncomment to test):
python synonymize.py -b -a expand $CANONICAL_NAMES > $EXPANDED_NAMES
diff -s <(sort $CANONICAL_NAMES) <(python synonymize.py -b -a merge -c $CANONICAL_NAMES $EXPANDED_NAMES | sort | uniq)

## output: Files /dev/fd/63 and /dev/fd/62 are identical

