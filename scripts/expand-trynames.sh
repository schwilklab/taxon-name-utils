#!/usr/bin/env bash

TRYNAMES="../data/name-lists/gbif-occurrences-names.txt"
EXPANDED_NAMES="../results/expanded-gbif-occurrences-names.txt"

python synonymize.py -a expand $TRYNAMES > $EXPANDED_NAMES

# to merge the result, in $EXPANDED NAMES
# python synonymize.py -a merge -c $TRYNAMES $EXPANDED_NAMES >> ../results/try-merged-names.txt

# proof this is reversible :
# diff -s <(sort $TRYNAMES) <(python synonymize.py -a merge -c $TRYNAMES $EXPANDED_NAMES | sort | uniq)

## output: Files /dev/fd/63 and /dev/fd/62 are identical

