#!/usr/bin/env bash

TANKNAMES="../data/name-lists/tank-tree-names.txt"
EXPANDED_NAMES="../results/expanded-tank-tree-names.txt"

python synonymize.py -a expand $TANKNAMES > $EXPANDED_NAMES
# or, with -b option 
# python synonymize.py -b -a expand $TANKNAMES > $EXPANDED_NAMES

