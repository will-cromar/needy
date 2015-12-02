import newspaper
import time
from sentiment_analysis import guessSentiment

paper = newspaper.build('http://www.foxnews.com/', memoize_articles=False)
print paper.size()

for article in paper.articles:
    article.download()
    article.parse()
    article.nlp()
    print article.title
    print article.summary
    print guessSentiment(article.text)
    print "-----------------------------"
