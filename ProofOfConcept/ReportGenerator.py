from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from scrapy.commands import crawl
from sklearn.tree import tree
from ProofOfConcept.fetch import getNews, summarize
from ProofOfConcept.graph_test_func import graphNN
from news import overallSentiment
from price_parsing import getStockPrices, preprocessStocks
from regression_graphs import graphRegressionsOverTime
from regression_models import Dataset, runRegressions

__author__ = 'tylervanharen'
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import requests

def hello(c):
    c.drawString(100,100,'Hello World');

def genReport(company):
    report = canvas.Canvas(company+".pdf",pagesize=letter);
    width,height = letter;
    report.setFont("Helvetica",30)
    report.drawCentredString(width/2,725*height/800,getCompanyName(company));
    report.setFont("Helvetica",17);
    report.drawCentredString(width/2,700*height/800,"("+company+")");
    report.line(width/32,43*height/50,31*width/32,43*height/50);
    report.line(width/16,42*height/50,15*width/16,42*height/50);

    # data = getStockPrices(company, frequency="daily");
    # times, prices = preprocessStocks(data);
    # dataset = Dataset(times, prices, company, graphColor="k", mode="sklearn");
    #
    # min_samples = len(times) * .025;
    #
    # regs = [("Decision tree", tree.DecisionTreeRegressor(min_samples_leaf=min_samples), "r")];
    #         #("Ouija board", svm.SVR(kernel="poly"), "g")]
    #
    # regressions = runRegressions(regs, times, prices);
    # graphRegressionsOverTime(company, dataset, *regressions);
    print("Creating report on "+company);
    graphNN(company,'11/24/15',2000)
    report.drawImage(company+".png",1.75*width/10,35*height/80,height=310,width=400);
    report.setFont("Helvetica",25)
    report.drawCentredString(3*width/10,height/3+50,"In The News:");
    newsUrls = getNews(getCompanyName(company),4)
    positivity = overallSentiment(newsUrls,verbose=True);

    #report.setFillColorRGB(255*(1-positivity),255*positivity,0);
    report.drawCentredString(6*width/10,height/3+50,str(100*positivity)+"% Positive");
    #report.setFillColorRGB(0,0,0);
    report.setFont("Helvetica",8);
    styleSheet = getSampleStyleSheet();
    body = styleSheet['BodyText'];
    body.fontSize = 8;
    for i in range(0,3):
        P = Paragraph(summarize(newsUrls[i]),body);
        w,h = P.wrap(width/3.5,height/10);
        P.drawOn(report,i*width/3+20,height/3-h+20);
    #report.drawCentredString(4*width/10,height/5,summarize(newsUrls[1]));
    report.showPage();
    report.save();

def getCompanyName(ticker):
    yahoo = requests.get("http://d.yimg.com/autoc.finance.yahoo.com/autoc?query="+ticker+"&region=1&lang=en");
    yjson = yahoo.json();
    return yjson["ResultSet"]["Result"][0]["name"];



dji = ["MMM","AXP","AAPL","BA","CAT","CVX","CSCO","KK","DD","XM","GE"]

for i in ['GOOG']:
    genReport(i);
