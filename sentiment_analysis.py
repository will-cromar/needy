import string

import util

from sklearn.datasets import load_files
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import *
from nltk.stem.snowball import SnowballStemmer

SENTIMENT_CLF = "sentiment_clf"
REVIEWS = "movie_reviews"


def stemmedWords(text):
    stemmer = SnowballStemmer("english")
    stemmedText = [stemmer.stem(word) for word in text.split()
                       if word not in string.punctuation]
    return " ".join(stemmedText)

def preprocessedMovieReviews():
    movieReviews = load_files("ProofOfConcept/txt_sentoken", shuffle=False)


    processedData = []
    textData = movieReviews.data
    for text in textData:
        processedData.append(stemmedWords(text))

    return processedData, movieReviews.target

def constructClassifier():
    data = None
    if not util.pickleExists(REVIEWS):
        data = preprocessedMovieReviews()
        util.savePickle(data, REVIEWS)
    else:
        data = util.getMostRecentPickle(REVIEWS)

    features, labels = data
    X_train, X_test, y_train, y_test = \
        train_test_split(features, labels, test_size=.2, random_state=42)

    textClf = Pipeline([("Vectorizer", TfidfVectorizer(stop_words="english")),
                        ("Classifier", LinearSVC(C=1.25))])

    textClf.fit(X_train, y_train)
    y_pred = textClf.predict(X_test)
    print "Training finished. Classifier accuracy:", accuracy_score(y_test, y_pred)

    util.savePickle(textClf, SENTIMENT_CLF)

    return textClf

def guessSentiment(text):
    clf = util.getMostRecentPickle(SENTIMENT_CLF)
    res = clf.predict([stemmedWords(text)])

    if res[0] == 1:
        return "Positive"
    else:
        return "Negative"