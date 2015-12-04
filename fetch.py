import urllib2
import simplejson
from newspaper import Article


def getNews(company, num):
    urls= []
    keyBing = 'TKr6QzuNP0P6RxsdZy/ddGeWc5Vf6dXX7UWPR9CD8XY'
    credentialBing = 'Basic ' + (':%s' % keyBing).encode('base64')[:-1] # the "-1" is to remove the trailing "\n" which encode adds
    searchString = validizeCompany(company)
    top = num
    offset = 0
    url = 'https://api.datamarket.azure.com/Bing/Search/v1/News?' + \
      'Query=%s&$top=%d&$skip=%d&$format=json' % (searchString, top, offset)
    request = urllib2.Request(url)
    request.add_header('Authorization', credentialBing)
    requestOpener = urllib2.build_opener()
    response = requestOpener.open(request)
    results = simplejson.load(response)
    for i in range(0, num):
        try:
            print str(i)+". "+str(results['d']['results'][i]['Url'])
            urls.append(results['d']['results'][i]['Url'])
        except:
            print("Failed to find article "+str(i))
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
    return "%27"+company.replace(" ", "+")+"%27"

