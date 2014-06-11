###script to pull synonyms off the plant list for each accepted name in the plant list v1.1
###Accepted names list was generated using the build.R and theplantlist.R scripts adapated from R. Fitzjohn's woodiness scripts on github
###written by EJ Forrestel, 1 April 2014

require(RCurl,quiet=TRUE)
require(doMC)
registerDoMC(12)

setwd("~/Desktop/ThePlantList_V1.1/data/theplantlist")

names <- read.csv("names_accepted.csv")

path <- "data/theplantlist"
dir.create(file.path(path, "synonymsNames1.1"), FALSE)
setwd("synonymsNames1.1")

file_name <- "TPL1.1_synonymy_list"
write.table(NULL,file=file_name)


plant.list.url <- function(ID) {
	
  	plant.list.url <- sprintf("http://www.theplantlist.org/tpl1.1/record/%s",ID)
	dat <- getURLContent(plant.list.url)
	return(dat)
	
}


get.synonyms <- function(i){
	
	species <- as.character(names[i,'gs'])
	ID <- names[i,'ID']
	print(paste(i,species,sep="_"))
	dat <- plant.list.url(ID)
	m <- gregexpr('</p>\n+<h2>Synonyms:</h2>.*',dat)
	if(m[[1]]==-1){message(paste0(species," does not exist in The Plant List as spelled"))}
	sub <- regmatches(dat,m)[[1]]
	sp.reg <- '<span class=\"name\"><i class=\"genus\">([A-Za-z\\s]+)</i> <i class=\"species\">(\\w+)</i> <span class=\"authorship\">'
	subsp.reg <- '<span class=\"name\"><i class=\"genus\">([A-Za-z\\s]+)</i> <i class=\"species\">([a-z-]+)</i> <span class=\"infraspr\">([a-z]+\\.)</span> <i class=\"infraspe\">(\\w+)</i> <span class=\"authorship\">'
	hyb.reg <- '<span class=\"name\"><i class=\"genus\">([A-Za-z\\s]+)</i> <i class=\"specieshybrid\">(×)</i>&nbsp;<i class=\"species\">(\\w+)</i> <span class=\"authorship\">'
	sp <- gregexpr(sp.reg,sub)
	match.sp <- unlist(regmatches(sub,sp))
	if(length(match.sp)>0){synonyms.sp <- gsub(sp.reg,'\\1_\\2',match.sp)}else{synonyms.sp <- NULL} 
	subsp <- gregexpr(subsp.reg,sub)
	match.subsp <- unlist(regmatches(sub,subsp))
	if(length(match.subsp)>0){synonyms.subsp <- gsub(subsp.reg,'\\1_\\2_\\3_\\4',match.subsp)}else{synonyms.subsp <- NULL}
	hyb <- gregexpr(hyb.reg,sub)
	match.hyb <- unlist(regmatches(sub,hyb))
	if(length(match.sp)>0){synonyms.hyb <- gsub(hyb.reg,'\\1_\\2_\\3',match.hyb)}else{synonyms.hyb <- NULL} 

	return(c(species,synonyms.sp,synonyms.subsp,synonyms.hyb))
	
}



foreach(i=1:nrow(names)) %dopar% {
	
	syn_spp <- get.synonyms(i)
	syn_spp <- gsub(" ","",toString(syn_spp))
	write.table(syn_spp,file=file_name,append=TRUE,col.names=FALSE,row.names=FALSE,quote=FALSE)
	
}


