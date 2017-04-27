#!/usr/bin/env bash

CANONICAL_NAMES="../data/name-lists/tank-tree-names.txt"
EXPANDED_NAMES="../results/expanded-tank-tree-names.txt"

python synonymize.py -b -a expand $CANONICAL_NAMES > $EXPANDED_NAMES
