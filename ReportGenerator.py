from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Paragraph
from reportlab.pdfbase.ttfonts import TTFont
from recent_trend import graphRecentTrend

from fetch import getNews,  summarize
from ProofOfConcept.graph_test_func import graphNN
from sentiment_analysis import overallSentiment

__author__ = 'tylervanharen'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import requests

def genReport(company, runs, newsCount):
    print "starting generation with ", runs, " runs and ", newsCount, " articles."
    report = canvas.Canvas(company+".pdf", pagesize=letter)
    #Embedding the font into the pdf so it can render
    ttfFile = "Humor-Sans-1.0.ttf"
    pdfmetrics.registerFont(TTFont("HumorSans",  ttfFile))

    width, height = letter

    #Drawing blue background on pdf
    report.setFillColor(HexColor('#345592'))
    report.setStrokeColor(HexColor('#91A2C4'))
    report.rect(0, 0, width, height, fill=True)
    report.setFillColor(HexColor('#91A2C4'))

    #Writing heading to top of PDF with lines beneath for aesthetics
    report.setFont("HumorSans", 30)
    report.drawCentredString(width/2, 725*height/800, getCompanyName(company))
    report.setFont("HumorSans", 17)
    report.drawCentredString(width/2, 700*height/800, "("+company+")")
    report.line(width/32, 43*height/50, 31*width/32, 43*height/50)
    report.line(width/16, 42*height/50, 15*width/16, 42*height/50)


    print("Creating report on "+company)

    #Generating .pngs of the predictions from the Neural Net and Linear approximation, respectively
    predictedPrice = graphNN(company, '11/24/15', runs, True)[0]
    graphRecentTrend(company)

    #Put the .pngs on the report, below the aesthetic lines of the header. NN on the right, linear on the left
    report.drawImage(company+"NN.png", 4.8*width/10, 36*height/80, height=300, width=300, mask='auto')
    report.drawImage(company+"linear.png", 1*width/10, 42*height/80, height=200, width=200, mask='auto')
    report.setFont("HumorSans", 25)
    report.drawCentredString(4.5*width/10,height/3+75,"Predicted Price: $ %.2f" %predictedPrice)

    #Drawing news summaries
    newsUrls = getNews(getCompanyName(company), newsCount)

    #If we failed to download news articles, we will avoid drawing any of the news section
    if(len(newsUrls) > 0):

        #Summary of the percieved positivity of all grabbed articles. (Num positive / num articles)
        report.drawCentredString(3*width/10, height/3+45, "In The News:")
        positivity = overallSentiment(newsUrls, verbose=True)
        report.drawCentredString(6*width/10, height/3+45, str(100*positivity)+"% Positive")

        report.setFont("HumorSans", 8)

        #Getting the paragraph form set up for writing summaries
        styleSheet = getSampleStyleSheet()
        body = styleSheet['BodyText']
        body.fontSize = 8
        body.fontName = "HumorSans"
        body.textColor = HexColor('#91A2C4')

        #Writes summaries for the first three(or less if less retrieved) articles at the bottom of the page
        for i in range(0, min(3,len(newsUrls))):
            P = Paragraph(summarize(newsUrls[i]), body)
            w, h = P.wrap(width/3.5, height/10)
            P.drawOn(report, (i-1)*width/3+20, height/3-h+15)

    #Saves the report so the user can access it
    report.showPage()
    report.save()

def getCompanyName(ticker):
    yahoo = requests.get("http://d.yimg.com/autoc.finance.yahoo.com/autoc?query="+ticker+"&region=1&lang=en")
    yjson = yahoo.json()
    return yjson["ResultSet"]["Result"][0]["name"]
