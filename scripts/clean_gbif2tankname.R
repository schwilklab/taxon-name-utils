#!/usr/env Rscript

library(stringr)

## Dylan Schwilk

## clean the results for running the gbif2tankname fuzzy matching script. That
## script intentially overmatches. Easiest solution: identify "suspects"
## according to JW similarities. Keep clear gender switches, cull all suspect
## matches in which both names are a TPL name as those are probably false
## positives.

gbif2tank <-  read.csv("../results/gbif_tank_lookup_140610.txt", stringsAsFactors=FALSE)
names(gbif2tank) <- c("gbif","tank", "genus_jw", "se_jw", "gswitch")
fmatches <- subset(gbif2tank, tank!=gbif)
length(fmatches$gbif)


allgbif <- read.csv("../data/name-lists/gbif-occurrences-names.txt", header=FALSE, stringsAsFactors=FALSE)$V1
unmatched <- allgbif[! allgbif %in% gbif2tank$gbif]
length(unmatched)
length(gbif2tank$gbif)

## hyphens <- grepl("-", unmatched, fixed=TRUE)
## drophyphen <-  str_split_fixed(unmatched[hyphens], "-", 2)[,1]
## head(drophyphen)

tpl <- read.csv("../data/theplantlist1.1/names_unique.csv", stringsAsFactors=FALSE)
tpl <- paste(tpl$genus, tpl$species)


# names that are both TPL names, could be wrong
gbif2tank$bothtpl <- gbif2tank$gbif != gbif2tank$tank &
    (gbif2tank$gbif %in% tpl & gbif2tank$tank %in% tpl) 

# other suspects
gbif2tank$suspect <- gbif2tank$genus_jw < 0.96 |  gbif2tank$se_jw < 0.96

# rule for removal:
gbif2tank$remove <- gbif2tank$bothtpl & gbif2tank$suspect & 
        ( gbif2tank$gswitch != "True" )


remove <- subset(gbif2tank, remove)
length(remove$gbif)

keep <- subset(gbif2tank, !remove)
keep <- keep[with(keep,order(se_jw)),]
length(subset(keep, se_jw < 0.96)$gbif)

# now manually check other suspects!

write.csv(gbif2tank, "../data/name-lists/gbif_tank_lookup_140610_cleaned.csv", row.names=FALSE)

