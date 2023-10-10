#! /usr/bin/Rscript

# Code to take raw World Flora ONline data download
# (http://www.worldfloraonline.org/downloadData) and format a synonym list that
# is simple for the existing python synonymize.py to use.

# Dylan Schwilk 2022

library(data.table)
library(dplyr)

print("reading data")

# backbone data v.2022.07	Jul. 12, 2022 downloaded on 2022-08-22.
wfo <- fread("classification.txt", quote="")
wfo <- filter(wfo, taxonRank %in% c("SPECIES", "VARIETY", "SUBSPECIES"))
wfo <- select(wfo, taxonID, scientificName, taxonomicStatus, acceptedNameUsageID)
accepteds <- wfo %>% filter(taxonomicStatus=="ACCEPTED")
print("writing synonym list")

# 424225 accepteds

sink("WFO_synonyms_list")
for (id in accepteds$taxonID) {
  accepted <- wfo[which(wfo$taxonID==id)]$scientificName
  syns <- paste(wfo[which(wfo$acceptedNameUsage==id ),]$scientificName, collapse=",")
  cat(paste(accepted, ",", syns, "\n", sep=""))
  }
  
sink()
    
