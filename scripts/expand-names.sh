#!/usr/bin/env bash

CANONICAL_NAMES="../data/name-lists/tank-tree-names.txt"
EXPANDED_NAMES="../results/new-expanded-tank-tree-names.txt"

python2 synonymize.py -a expand $CANONICAL_NAMES > $EXPANDED_NAMES
