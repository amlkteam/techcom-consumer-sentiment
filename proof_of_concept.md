Corpus collection POC (proof-of-concept)

#Python code to collect Chinese texts from Weibo is found below:

https://github.ubc.ca/shuning3/COLX523_SH_VT_AL/blob/amylam/weibo_scrap_test.py

#Python code to collect English and French texts from Twitter: 

https://github.ubc.ca/shuning3/COLX523_SH_VT_AL/blob/amylam/twitter_apple_scrap_string.csv

#Step-by-step algorithm to create the corpus

## run python scripts to scrap Twitter and Weibo every day within rate limits
- if lang == En or lang == Fr:
      for each of the 5 companies:
             use twitter search api with geolocation and lang argument to identify relevant tweets
             do preprocessing on tweets to extract features/metadata 
             write(or append) one csv file 
  elif lang = Chinese:
            for each of the 5 companies:
             use Weibo Search page/Weibo API(need developer a/c) to extract relevant posts
             do preprocessing on tweets to extract features/metadata 
             write(or append) one csv file 

## Sentiment analysis
- for each sentence collected in the csv files:
       word tokenize, remove irrelevant words/stopwords
       use TextBlob/Spacy/cosine-similarity_of_word_embedding to get the sentiment polarity

## Annotations
- for each sentence collected in csv files:
      manually label sentiment partly by ourselves and partly by crowdsourcing

## Merge and Cleanup inconsistencies
