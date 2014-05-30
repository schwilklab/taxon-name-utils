#!/usr/bin/env bash

GBIFNAMES="../data/name-lists/gbif-occurrences-names.txt"
EXPANDED_NAMES="../results/expanded-gbif-occurrences-names.txt"

python synonymize.py -a expand $GBIFNAMES > $EXPANDED_NAMES

# to merge the result, in $EXPANDED NAMES
# python synonymize.py -a merge -c $GBIFNAMES $EXPANDED_NAMES >> ../results/gbif-merged-names.txt

# proof this is reversible :
# diff -s <(sort $GBIFNAMES) <(python synonymize.py -a merge -c $GBIFNAMES $EXPANDED_NAMES | sort | uniq)

## output: Files /dev/fd/63 and /dev/fd/62 are identical

