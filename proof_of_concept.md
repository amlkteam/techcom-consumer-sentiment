# Corpus collection POC (proof-of-concept)

## Demo codes

### Python code to collect Chinese texts from Weibo is found below:

https://github.ubc.ca/shuning3/COLX523_SH_VT_AL/blob/amylam/weibo_scrap_test.py

### Python code to collect English and French texts from Twitter is found here: 

https://github.ubc.ca/shuning3/COLX523_SH_VT_AL/blob/amylam/tweepy_test.py

## Step-by-step algorithm to create the corpus

### 1. run python scripts to scrap Twitter and Weibo every day within rate limits
corpus_word_size = 0
 while corpus_word_size < 1 million: 
   if lang == En or lang == Fr:

        for each of the 5 companies:

               use twitter search api with geolocation and lang argument to identify relevant tweets

               do preprocessing on tweets to extract features/metadata 

               write(or append) to csv file 

    elif lang = Chinese:

              for each of the 5 companies:

               use Weibo Search page or Weibo API(need developer a/c) to extract relevant posts

               do preprocessing on weibo posts to extract features/metadata 

               write(or append) to csv file 
    corpus_word_size += len(total_text)            

### 2. Sentiment analysis
- for each sentence collected in the csv files:

       tokenize into words, remove irrelevant words/stopwords, join filtered words to a new string
       
       use TextBlob/Spacy/Sentiment Axis(cosine-similarity of word embeddings) to get the sentiment polarity

### 3. Annotations
- for each sentence collected in csv files:

      manually label sentiment, identity of user, and purpose of post partly by ourselves and partly by crowdsourcing

### 4. Merge and Cleanup inconsistencies

