import newspaper
import time
from sentiment_analysis import guessSentiment

t0 = time.clock()
paper = newspaper.build('http://www.foxnews.com/', memoize_articles=False)
t1 = time.clock()
print t1 - t0
print paper.size()

for article in paper.articles:
    article.download()
    article.parse()
    article.nlp()
    print article.summary;
    print guessSentiment(article.text);
    print "-----------------------------"
