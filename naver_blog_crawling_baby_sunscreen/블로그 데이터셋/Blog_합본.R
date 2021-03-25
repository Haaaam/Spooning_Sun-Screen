setwd("/Users/dean/R/data")

# KoNLP 패키지
library(KoNLP)

suncream1 <- readLines("/Users/dean/R/data/유아썬크림_검색결과.txt")
suncream2 <- readLines("/Users/dean/R/data/어린이썬크림_검색결과.txt")
suncream3 <- readLines("/Users/dean/R/data/아기썬크림_검색결과.txt")

suncream_all <- c(suncream1, suncream2, suncream3)
str(suncream_all)
head(suncream_all)

# 데이터 전처리
## - 중복된 값 제거
data_all <- unique(suncream_all)
head(data_all)
## - 특수문자 제거
library(stringr)
data_all <- str_replace_all(data_all, "[^[:alpha:][:blank:]]","")
head(data_all)

# 단어 단위로 분리
data_all_noun <- extractNoun(data_all)
head(data_all_noun, 100)
str(data_all_noun)

# 한 줄 안에서 중복되는 단어 제거
data_all_noun <- sapply(data_all_noun, unique)
str(data_all_noun)

# 띄어 쓰기가 안되어 있는 긴 문장(단어)을 제거
## - Filter() 함수에는 데이터가 벡터어야 한다
## - 그래서 unlist() 함수로 list -> vector 전환
data_all_vector <- unlist(data_all_noun) ; data_all_vector

# 불용어 제거
vector <- gsub("<(\\/?)(\\w +)*([^<>]*)>", "", data_all_vector)
vector <- gsub("[[:punct:]]", "", vector)
vector <- gsub("[a-z]", "", vector)
vector <- gsub("[0-9]", "", vector)
vector <- gsub(" +", "", vector)

vector <- Filter(function(x) {
  nchar(x) <= 10 & nchar(x) > 1}, vector) # 공백 제거
vector

# 불필요한 특정 단어 정의
excluNouns <- c('아이','썬크림','아기','아기썬크림','유아썬크림','우리','하기','어린이',
                '추천','해서','들이','유아','베이비','선크림','화장품','때문','하나','정도',
                '가지','썬크림을','썬크','경우','썬크림은','자외선차단제','저자','선크림을',
                '어린이썬크림','사실')
# 제거
vector <- vector[!vector %in% excluNouns]

# 추출된 키워드를 임시로 확인하기 위해 집계
wordcount <- table(vector)
head(sort(wordcount, decreasing = T),50)
wordcount <- head(sort(wordcount, decreasing = T),50)
wordcount

# WordCloud
library(wordcloud2)

wordcloud2(data = wordcount, color = "random-light", size = 0.7, shape = "diamond")
