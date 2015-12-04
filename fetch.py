import urllib2
import simplejson
from newspaper import Article


def getNews(company, num):
    """
    Uses Bing to find the url of news articles regarding a company
    :param company: The full name of the company for which news should be found
    :param num: The number of articles that should be found about the company
    :return: A list of urls to news articles regarding the company
    """
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
    """
    Generates a summary of the article at a given url
    :param url: The url of the article to be summarized
    :return: A summary of the article as a string
    """
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
    """
    Formats strings to allow for them to be included in the url of a search
    :param company: The string, in this case, generally the name of the company
    :return: The string, formatted to be in a query in the url.
    """
    return "%27"+company.replace(" ", "+")+"%27"

