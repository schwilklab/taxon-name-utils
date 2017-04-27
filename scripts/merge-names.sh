#!/usr/bin/env bash

CANONICAL_NAMES="../data/name-lists/tank-tree-names.txt"
EXPANDED_NAMES="../results/expanded-tank-tree-names.txt"

# to merge the result, in $EXPANDED NAMES
python synonymize.py -b -a merge -c $CANONICAL_NAMES $EXPANDED_NAMES > ../results/merged-names.txt
