import requests
import string
import justext

import util

from sklearn.datasets import load_files
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import *
from nltk.stem.snowball import SnowballStemmer

# Names of sentiment classifier and preprocessed movie reviews dataset, respectively, in cache
SENTIMENT_CLF = "sentiment_clf"
REVIEWS = "movie_reviews"

def stemmedWords(text):
    """
    Stems all words in text and removes punctuation. See SnowballStemmer in NLTK
    :param text: string of text to process
    :return: String of processed text
    """
    stemmer = SnowballStemmer("english") # Stemmer instance

    # Stem each word that is not punctuation, and store in list
    stemmedText = [stemmer.stem(word) for word in text.split()
                       if word not in string.punctuation]

    # Join each stemmed word with a space
    return " ".join(stemmedText)

def preprocessedMovieReviews():
    """
    Process sklearn's movie reviews corpus, stemming all words
    :return: List of processed movie review texts, list of labels
    """
    # Load reviews and labels from corpus. This is not stored in the repo. See your sklearn/docs/tutorial folder.
    # Warning: This will throw an exception if the folder is not there
    movieReviews = load_files("ProofOfConcept/txt_sentoken", shuffle=False)

    # Stem each review and add to processed data list
    processedData = []
    textData = movieReviews.data
    for text in textData:
        processedData.append(stemmedWords(text))

    # Returns data in form X, y
    return processedData, movieReviews.target

def constructClassifier(verbose=False):
    """
    Creates and caches sentiment analysis classifier base on movie reviews data. Review data is pulled
    from cache, so this will not work if you do not have the correct working directory structure. Will
    put the preprocessed movie reviews in repo so you guys don't need to download the corpus.
    :return: the created classifier (or -1 upon error)
    """
    # Get preprocessed movie review data
    data = None
    if not util.pickleExists(REVIEWS):
        data = preprocessedMovieReviews()
        util.savePickle(data, REVIEWS)
    else:
        data = util.getMostRecentPickle(REVIEWS)

    # Break if review data is not found
    if not data:
        print "Review data not found."
        return -1

    # Extract features and labels and create train/test sets
    features, labels = data
    X_train, X_test, y_train, y_test = \
        train_test_split(features, labels, test_size=.2, random_state=42)

    # Create pipeline, to tokenize, vectorize, transform, and classify data
    textClf = Pipeline([("Vectorizer", TfidfVectorizer(stop_words="english")),
                        ("Classifier", LinearSVC(C=1.25))])

    # Train the classifier
    if verbose: print "Training classifier..."
    textClf.fit(X_train, y_train)

    # Print accuracy score if verbose flag is no
    if verbose:
        y_pred = textClf.predict(X_test)
        print "Training finished. Classifier accuracy:", accuracy_score(y_test, y_pred)

    # Cache the classifier
    util.savePickle(textClf, SENTIMENT_CLF)

    return textClf

def guessSentiment(text):
    """
    Guesses the sentiment of given text
    :param text: String of text to analyze
    :return: "Positive" for positive sentiment, "Negative" for negative sentiment, -1 for error
    """
    clf = util.getMostRecentPickle(SENTIMENT_CLF)
    if not clf:
        print "Classifier not found"
        return -1

    # Predicted sentiment value of text. Note that this is a list because of how
    # sklearn wrote classifiers
    result = clf.predict([stemmedWords(text)])

    if result[0] == 1:      # 1: Positive sentiment
        return "Positive"
    else:                   # 0: Negative sentiment
        return "Negative"

def overallSentiment(urls, verbose=False):
    """
    Guesses the overall sentiment of the given articles
    :param urls: List of URLs of articles to read
    :param verbose: Print status updates and specific verdicts
    :return: The proportion of articles that are positive
    """
    sentiments = []

    for url in urls:
        try:
            if verbose: print "Downloading", url + "..."
            response = requests.get(url)
            paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
            allText = "\n".join([paragraph.text for paragraph in paragraphs])
            if verbose: print "Reading..."
            sentiment = guessSentiment(allText)
            if verbose: print "Verdict:", sentiment
            sentiments.append(sentiment)
        except:
            if verbose: print "Failed to download", url


    positiveCount = len(filter(lambda x: x == "Positive", sentiments))
    return float(positiveCount) / len(urls)