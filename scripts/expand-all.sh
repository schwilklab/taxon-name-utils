#!/usr/bin/env bash

GBIFNAMES="../data/name-lists/gbif-occurrences-names.txt"
TANKNAMES="../data/name-lists/tank-tree-names.txt" 
EXPANDED_NAMES="../results/expanded-gbif-occurrences-names.txt"

python synonymize.py -a expand $TANKNAMES > $EXPANDED_NAMES
python synonymize.py -a expand $GBIFNAMES >> $EXPANDED_NAMES
