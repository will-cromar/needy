import urllib2
import newspaper
import simplejson
from newspaper import Article
from sentiment_analysis import guessSentiment, overallSentiment


def getNews(company, num):
    urls= []
    paper = newspaper.build('http://www.cnn.com/', memoize_articles=False)
    for i in range(0, num):
        urls.append(paper.article_urls()[i])
        # try:
        #     url = ('https://ajax.googleapis.com/ajax/services/search/news?' +
        #     'v=1.0&q='+validizeCompany(company)+'&userip=INSERT-USER-IP&start='+str(i*4))
        #     request = urllib2.Request(url,  None)
        #     response = urllib2.urlopen(request)
        #     print response
        #     # Process the JSON string.
        #     results = simplejson.load(response)
        #     print results
        #     for j in results['responseData']['results']:
        #         urls.append(j['unescapedUrl'])
        # except:
        #     print "Failed to load results from page ", (i+1)
    return urls

def summarize(url):
    a = Article(url)
    a.download()
    i = 0
    skip = False
    while not a.is_downloaded:
        if i>10:
            break
        i+=1
        a.download()
    if(not a.is_downloaded):
        return None
    i = 0

    a.parse()

    while not a.is_parsed:
        if i>10:
            skip = True
            break
        i+=1
        a.parse()
    if (not a.is_parsed):
        return None


    a.nlp()
    return a.summary

def validizeCompany(company):
    return company.replace(" ", "%20")


