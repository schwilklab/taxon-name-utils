shorten_word_string <- function(x,number_to_trim_to=2) {
  ul = unlist(strsplit(x, split = "\\s+"))[1:number_to_trim_to]
  paste(ul, collapse = " ")
}

get_number_words<-function(str1){
  sapply(gregexpr("[[:alpha:]]+", str1), function(x) sum(x > 0))
}

get_lookup_table <- function(names_of_interest) {
  require(dplyr)
  require(readr)
  names_of_interest_binom <-
    unlist(lapply(names_of_interest, shorten_word_string))
  
  nw <- get_number_words(names_of_interest) 
  names_of_interest[nw>4]<-shorten_word_string(names_of_interest[nw>4],4)
  
  write.table(
    names_of_interest,
    col.names = FALSE,
    quote=FALSE,
    row.names=FALSE,
    "../data/name-lists/orig_names.txt")

    system(
    'python2 ./synonymize.py -b -a expand ../data/name-lists/orig_names.txt > ../results/wrapper-expanded.txt'
  )
  system(
    'python2 ./synonymize.py -b -a merge -c ../data/name-lists/orig_names.txt ../results/wrapper-expanded.txt  > ../results/wrapper-merged-names.txt'
  )
  syn <-
    read.csv("../results/wrapper-expanded.txt",
             col.names = "syn",stringsAsFactors = FALSE)
  old_name <-
    read.csv("../results/wrapper-merged-names.txt", col.names = "old_name",stringsAsFactors = FALSE)
  good_names <-
    read.csv("../data/theplantlist1.1/names_unique.csv",stringsAsFactors = FALSE)
  good_names$binom <- paste(good_names$genus, good_names$species)
  df <- data_frame(old_binom = old_name$old_name, new_binom = syn$syn)
  #df_out <- filter(df, new_binom %in% good_names$binom)
  #  return(df_out)
  return(df)
} 
