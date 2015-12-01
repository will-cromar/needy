from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Paragraph
from reportlab.pdfbase.ttfonts import TTFont

from fetch import getNews, summarize
from ProofOfConcept.graph_test_func import graphNN
from news import overallSentiment


__author__ = 'tylervanharen'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import requests

def hello(c):
    c.drawString(100,100,'Hello World')

def genReport(company):
    runs = 5
    newsCount = 4
    print "starting generation with ",runs," runs and ",newsCount," articles."
    report = canvas.Canvas(company+".pdf",pagesize=letter)
    ttfFile = "Humor-Sans-1.0.ttf"
    pdfmetrics.registerFont(TTFont("HumorSans", ttfFile))
    width,height = letter
    report.setFillColor(HexColor('#345592'))
    report.setStrokeColor(HexColor('#91A2C4'))
    report.rect(0,0,width,height,fill=True)
    report.setFillColor(HexColor('#91A2C4'))
    report.setFont("HumorSans",30)
    report.drawCentredString(width/2,725*height/800,getCompanyName(company))
    report.setFont("HumorSans",17)
    report.drawCentredString(width/2,700*height/800,"("+company+")")
    report.line(width/32,43*height/50,31*width/32,43*height/50)
    report.line(width/16,42*height/50,15*width/16,42*height/50)
    print("Creating report on "+company)
    graphNN(company,'11/24/15',runs)
    report.drawImage(company+"NN.png",1.75*width/10,35*height/80,height=310,width=400,mask='auto')
    report.setFont("HumorSans",25)
    report.drawCentredString(3*width/10,height/3+50,"In The News:")
    newsUrls = getNews(getCompanyName(company),newsCount)
    positivity = overallSentiment(newsUrls,verbose=True)

    report.drawCentredString(6*width/10,height/3+50,str(100*positivity)+"% Positive")

    report.setFont("HumorSans",8)
    styleSheet = getSampleStyleSheet()
    body = styleSheet['BodyText']
    body.fontSize = 8
    body.fontName = "HumorSans"
    body.textColor = HexColor('#91A2C4')
    for i in range(0,3):
        P = Paragraph(summarize(newsUrls[i]),body)
        w,h = P.wrap(width/3.5,height/10)
        P.drawOn(report,i*width/3+20,height/3-h+20)
    #report.drawCentredString(4*width/10,height/5,summarize(newsUrls[1]))
    report.showPage()
    report.save()

def getCompanyName(ticker):
    yahoo = requests.get("http://d.yimg.com/autoc.finance.yahoo.com/autoc?query="+ticker+"&region=1&lang=en")
    yjson = yahoo.json()
    return yjson["ResultSet"]["Result"][0]["name"]



dji = ["MMM","AXP","AAPL","BA","CAT","CVX","CSCO","KK","DD","XM","GE","GS","HD","INTC","IBM","JNJ","JPM","MCD","MSFT","NKE","PFE","PG","TRV","UNH","UTX","VZ","V","WMT","DIS"]

for i in ['GOOG']:
    genReport(i)
