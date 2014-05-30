 #!/usr/bin/env bash

TANKNAMES="../data/name-lists/tank-tree-names.txt"
EXPANDED_NAMES="../results/expanded-tank-tree-names.txt"

python synonymize.py -a expand $TANKNAMES > $EXPANDED_NAMES

# to merge the result, in $EXPANDED NAMES
# python synonymize.py -a merge -c $TANKNAMES $EXPANDED_NAMES >> ../results/merged-names.txt

# proof this is reversible :
# diff -s <(sort $TANKNAMES) <(python synonymize.py -a merge -c $TANKNAMES $EXPANDED_NAMES | sort | uniq)

## output: Files /dev/fd/63 and /dev/fd/62 are identical

