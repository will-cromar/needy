4import newspaper
import time

t0 = time.clock()
paper = newspaper.build('http://abcnews.go.com/', memoize_articles=False)
t1 = time.clock()
print t1 - t0
print paper.size()

for article in paper.articles:
    article.download()
    article.parse()
    print article.publish_date
    print article.url
