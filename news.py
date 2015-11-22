import requests

from sentiment_analysis import guessSentiment

import justext

def overallSentiment(urls, verbose=False):
    sentiments = []

    for url in urls:
        if verbose: print "Downloading", url + "..."
        response = requests.get(url)
        paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
        allText = "\n".join([paragraph.text for paragraph in paragraphs])
        if verbose: print "Reading..."
        sentiment = guessSentiment(allText)
        if verbose: print "Verdict:", sentiment
        sentiments.append(sentiment)

    positiveCount = len(filter(lambda x: x == "Positive", sentiments))
    return float(positiveCount) / len(urls)


print overallSentiment(["http://www.financialmagazin.com/samsung-electronics-co-ltd-adr-stock-price-gaps-up-today-buyers-are-thriving/",
                       "http://www.financialmagazin.com/a-reversal-for-samsung-electronics-co-ltd-adr-is-not-near-the-stock-gaps-down/",
                       "http://www.businessinsider.com/how-to-buy-samsung-stock-2013-1",
                       "http://dazeinfo.com/2013/03/25/samsung-electronics-co-ltd-vs-nokia-corporation-adr-smartphone-market/",
                       "http://investcorrectly.com/20150417/samsung-electronics-co-ltd-attempts-emulate-apple-inc-pricing-model-expanding-memory/",
                       "http://seekingalpha.com/article/562611-primer-on-international-investing-part-2",
                       "http://seekingalpha.com/article/1082161-samsung-should-come-to-nyse-or-nasdaq",
                       "http://www.benzinga.com/general/education/15/07/5664682/the-pros-cons-of-buying-foreign-stocks-otc",
                       "http://investcorrectly.com/20150723/idc-samsung-elect-ltdf-ssnlfs-2q-smartphone-market-share-falls-apple-inc-gains-as-global-sales-rise-11-6/",
                       "http://investcorrectly.com/20150421/samsung-electronics-co-ltd-aims-grab-ssd-market-2015-talks-potential-customers-like-google-amazon-apple/"],
                       verbose=False)