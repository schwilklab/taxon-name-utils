taxon-name-utils
================

Code and data for plant name synonym expansion and fuzzy name matching. Most recent use is by the "mycorrhizal soil/climate" analyses, see the [plant_gbif repository](https://github.com/Fireandplants/plant_gbif)

Current release: [![DOI](https://zenodo.org/badge/20335477.svg)](https://zenodo.org/badge/latestdoi/20335477)

## Data ##

### The World Flora Online ###

We use the `classification.txt` data file downloaded from  [World Flora Online](http://www.worldfloraonline.org/downloadData). `/data/WFO_2_synonym_list.R` produces a reformatted file for `/scripts/synonymize.py`

### Name lists ###

`/data/name-lists/`: lists of names from other sources to match/scrub against. Provided as examples.

## Scripts ##

### Synonym expansion and merging ###

The `/scripts/synonymize.py` utility creates a synonym table from World Flora ONline. The idea is to hand the script a list of canonical names (such as the species names associated with your trait data), and obtain a list of names that includes those and all synonyms. For example:

```
python synonymize.py -b -a expand canonical_names.txt > expanded_names.txt
```

The command above uses the `-b` option to indicate we want to only use binomials and ignore three-part names, the `-a` option gives the action to perform (expand).

The merge action allows merging to a canonical list of names (not necessarily World Flora Online "accepted" names, although that is the default). The result will be of the same length as the input expanded names list but every name will be replaced with the corresponding canonical name.  By lining up the expanded list with the merged result one can create a lookup table that allows converting from any synonym to a canonical anme. You will always want to merge back to your original canonical names list:

```
python synonymize.py -b -a merge -c canonical_names.txt expanded_names.txt > ../results/merged-names.txt
```

See the docstring and usage for more information. Try:

```
python synonymize.py -h
```

This could be speeded up by cacheing the lookup dictionaries. As it works now, the entire lookup data is re-read each time the program is run. But it works.

The `expand_names.sh` provides an example usage expanding the canonical names from the [Tank tree][TankTree]. See [Zanne et al 2013][Zanne-etal-2013]. This is just an example. 

### Name matching ###

- `fuzzy_match.py` provides the `fuzzy_match_name_list()` function.
- `gbif_lookup.py` is an example script that demonstrates how to use the `fuzzy_match_name_list` function.  The script creates a lookup table from the expanded [Tank et al.][TankTree] tree names created by `expand_tanknames.sh` to the names found in the [gbif][GBIF] database according to `/data/names-lists/gbif-occurrences-names.txt`.

The code in the [plant_gbif repository](https://github.com/Fireandplants/plant_gbif) provides more complete examples of how to use taxon-name-utils for large name matching tasks.


[ejforrestel]: https://github.com/ejforrestel
[GBIF]: http://www.gbif.org/
[TPL]: http://www.theplantlist.org/
[TPL-accepted]: http://www.theplantlist.org/1.1/about/#accepted
[TankTree]: http://datadryad.org/resource/doi:10.5061/dryad.63q27/3
[Zanne-etal-2013]: http://www.nature.com/nature/journal/v506/n7486/full/nature12872.html
