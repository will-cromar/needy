import requests

from sentiment_analysis import guessSentiment

import justext

def overallSentiment(urls, verbose=False):
    """
    Guesses the overall sentiment of the given articles
    :param urls: List of URLs of articles to read
    :param verbose: Print status updates and specific verdicts
    :return: The proportion of articles that are positive
    """
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