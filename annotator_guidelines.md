# Annotator Guidelines

The following shall serve as guidelines for annotators working on the project titled 'A Sentiment Analysis of Big Tech on Twitter and Weibo.'

## The Task

The annotator will be presented with one Tweet at a time. The Tweet will be in one of three languages (English, French, or Chinese) and focus on one big tech company (Amazon, Microsoft, Facebook, or Apple). The annotator will read the text of the Tweet and decide if the tweet falls under one of six categories: Very positive, positive, neutral, negative, very negative, or irrelevant. We anticipate that completing this task will require about seven to ten seconds, depending on the length of the tweet.

## Guidelines 

The following is a detailed breakdown of the six possible categories.

#### Very Positive

If the Tweet displays a positive sentiment with high intensity, mark it as Very Positive. Look for clues such as exclamation marks, happy emojis, or expressions of pleasant surprise or excitement. 

Examples of tweets that are very positive:
- "Apple is the best company in the world!"
- "I love using Microsoft's services!"

#### Positive

If the Tweet displays a positive sentiment with low intensity, mark it as Positive. Look for words that express joy or delight, but which are less strong than those which would be marked as very positive.

Examples of tweets that are positive: 
- "Facebook is a nice company."
- "Apple makes pretty good phones."

#### Neutral

If the Tweet is neither positive nor negative, mark it as Neutral. Tweets that state a true fact may fall under this category.

Examples of tweets that are neutral:
- "Amazon is a very large company."
- "There are Amazon offices in Vancouver."

#### Negative

If the Tweet displays a negative sentiment with low intensity, mark it as Negative. They may contain words that express sadness, sarcasm, or anxiety. 

Examples of tweets that are negative: 
- "I think Facebook is stealing all of my data."
- "Apple products have a really short battery life."

#### Very Negative 

If the Tweet displays a negative sentiment with high intensity, mark it as Very Negative. Look for words that express anger, frustration, or desperation. Additionally, there may be clues such as exclamation marks or negative emojis. 

Examples of tweets that are very negative:
- "I hate Facebook!!!"
- "I think Amazon is a horrible company."

#### Irrelevant

Some Tweets may contain irrelevant content as a result of a lack of word sense disambiguation in our corpus collection methods. If the tweet's content isn't relevant to the company that it's supposed to be about, mark as Irrelevant and ignore any sentiment. 

Examples of tweets that are irrelevant: 
- "This is the most delicious apple I've ever eaten."
- "I'm so excited to visit the Amazon in Brazil!"

## Ambiguous Cases

In the case that a Tweet displays multiple emotions or the annotator is not sure whether a tweet is irrelevant or not, we suggest annotating with the category under which the stronger emotion falls. For example, if part of a tweet is slightly joyful but another part of a tweet is extremely sad, then the entire tweet would be marked as Negative because the sadness is conveyed more strongly than the joyfulness. We also encourage annotators to trust their judgement and intuition in ambiguous cases.

## Further Resources

Data in CSV format is available [here](https://github.ubc.ca/shuning3/COLX523_SH_VT_AL/blob/serena/data/twitter_french_results_last.csv). Annotators will see data in this format. The code that produced this data can be found [here](https://github.ubc.ca/shuning3/COLX523_SH_VT_AL/blob/serena/codes/french_twitter_scraping_final.ipynb).





