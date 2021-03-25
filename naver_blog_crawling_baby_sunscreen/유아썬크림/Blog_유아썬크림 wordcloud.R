sun <- readLines("/Users/dean/R/data/유아썬크림_검색결과.txt")
str(sun)
head(sun)

# KoNLP 패키지
library(KoNLP)

# 데이터 전처리
## - 중복된 값 제거
data1 <- unique(sun)
head(data1)
## - 특수문자 제거
install.packages("stringr")
library(stringr)
data1 <- str_replace_all(data1, "[^[:alpha:][:blank:]]","")
data1

# 단어 단위로 분리
data2 <- extractNoun(data1)
head(data2, 20)

# 한 줄 안에서 중복되는 단어 제거
data2 <- sapply(data2, unique)

# 띄어 쓰기가 안되어 있는 긴 문장(단어)을 제거
## - Filter() 함수에는 데이터가 벡터어야 한다
## - 그래서 unlist() 함수로 list -> vector 전환
data3 <- unlist(data2) ; data3

data4 <- Filter(function(x) {
  nchar(x) <= 10 & nchar(x) > 1}, data3)
data4

# 불용어 제거
data4 <- gsub("<(\\/?)(\\w +)*([^<>]*)>", "", data4)
data4 <- gsub("[[:punct:]]", "", data4)
data4 <- gsub("[a-z]", "", data4)
data4 <- gsub("[0-9]", "", data4)
data4 <- gsub(" +", "", data4)

data4 <- Filter(function(x) {
  nchar(x) <= 10 & nchar(x) > 1}, data4) # 공백 제거
data4

# 불필요한 특정 단어 정의
excluNouns <- c('썬크림','선크림','추천','하기','해서','들이','썬크','때문','썬크림을',
                '하나')
# 제거
data4 <- data4[!data4 %in% excluNouns]

# 추출된 키워드를 임시로 확인하기 위해 집계
wordcount <- table(data4)
wordcount <- head(sort(wordcount, decreasing = T),50)
wordcount

# WordCloud
library(wordcloud2)

wordcloud2(data = wordcount, size = 0.8, shape = 'diamond')
