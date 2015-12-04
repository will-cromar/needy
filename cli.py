import ReportGenerator
from sys import stdin

# Entry point for Needy

import nltk
nltk.data.path.append("/home/will/build/nltk_data")

while True:
    # Get the ticker name
    print "Enter the name of a stock ticker, or \"exit\""
    ticker = stdin.readline()
    ticker = ticker[0:-1] # eat the newline

    # Let the user exit
    if ticker == "exit":
        exit(0)

    # If the company does not exist, restart loop
    try:
        company = ReportGenerator.getCompanyName(ticker)
    except:
        print "Not a valid ticker"
        continue

    # Get the number of runs for the neural network
    print "Enter a number of NN runs > 1"
    runs = None
    try:
        runs = int(stdin.readline())
        if not runs > 1:
            print "Invalid. Defaulting to 2."
            runs = 2
    except:
        print "Not a valid int"
        continue

    # Get the numer of articles to read and classify
    print "Enter a number of articles >= 4"
    articles = None
    try:
        articles = int(stdin.readline())
        if not articles >= 4:
            print "Invalid. Defaulting to 4."
            articles = 4
    except:
        print "Not a valid int"
        continue

    # Finally, put the report together with the given options
    print "Building report for", company
    ReportGenerator.genReport(ticker, runs, articles)