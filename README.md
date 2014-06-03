taxon-name-utils
================

Code and data for plant name synonym expansion and name matching

## Data ##

### The Plant List ###

This is stored at `/data/theplantlist1.1`.  Scraped from [The Plant List][TPL]by [Beth Forrestel][ejforrestel] around 3/30/2014.

- /data/theplantlist1.1/families/: lists of all family names by phylum
- /data/theplantlist1.1/names_unique.csv: All unique plant names in [The Plant List][TPL].  TODO: add metadata on variables
- /data/theplantlist1.1/TPL1_1_synonymy_list: Synonymy list as a ragged array; comma-separated.  First item is an [accepted name][TPL-accepted].  This is followed by a comma-separated list of synonyms.


### Name lists ###

`/data/name-lists/`: lists of names from other sources to match/scrub against.

## Scripts ##

### Synonym expansion and merging ###

The `/scripts/synonymize.py` utility creates a synonym table from The Plant List data.

It allows expansion of a names list to a larger list including those names and all
synonyms. The merge action allows merging to a canonical list of names (not
necessarily TPL accepted names, although that is the default).

See the docstring and usage for more information.

This could be speeded up by cacheing the lookup dictionaries. As it works now,
the entire lookup data is re-read each time the program is run. But it works.

The `expand_tanknames.sh` provides an example usage expanding the canonical names from the [Tank tree][TankTree]. See [Zanne et al 2013][Zanne-etal-2013]. 

### Name matching ###

- `fuzzy_match.py` provides the fuzzy_matches() function.
- `gbif_lookup.py` provides a simplistic way to create a a lookup table from the expanded tank tree names created by `expand_tanknames.sh` to the names found in the gbif database accordidng to `/data/names-lists/gbif-occurrences-names.txt`.


[ejforrestel]: https://github.com/ejforrestel
[TPL]: http://www.theplantlist.org/
[TPL-accepted]: http://www.theplantlist.org/1.1/about/#accepted
[TankTree]: http://datadryad.org/resource/doi:10.5061/dryad.63q27/3
[Zanne-etal-2013]: http://www.nature.com/nature/journal/v506/n7486/full/nature12872.html
