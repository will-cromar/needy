import ReportGenerator
from sys import stdin

while True:
    print "Enter the name of a stock ticker, or \"exit\""
    ticker = stdin.readline()
    ticker = ticker[0:-1]

    if ticker == "exit":
        exit(0)

    try:
        company = ReportGenerator.getCompanyName(ticker)
    except:
        print "Not a valid ticker"
        continue

    print "Building report for", company
    ReportGenerator.genReport(ticker)