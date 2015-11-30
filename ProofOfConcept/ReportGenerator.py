from scrapy.commands import crawl
from sklearn.tree import tree
from ProofOfConcept.fetch import getNews
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

    data = getStockPrices(company, frequency="daily");
    times, prices = preprocessStocks(data);
    dataset = Dataset(times, prices, company, graphColor="k", mode="sklearn");

    min_samples = len(times) * .025;

    regs = [("Decision tree", tree.DecisionTreeRegressor(min_samples_leaf=min_samples), "r")];
            #("Ouija board", svm.SVR(kernel="poly"), "g")]

    regressions = runRegressions(regs, times, prices);
    graphRegressionsOverTime(company, dataset, *regressions);

    report.drawImage(company+".png",width/8,45*height/80,height=200,width=200);
    report.setFont("Helvetica",25)
    report.drawCentredString(width/4,height/4,"In The News:");
    positivity = overallSentiment(getNews(getCompanyName(company)),verbose=True);
    report.setFillColorRGB(255*(1-positivity),255*positivity,0);
    report.drawCentredString(6*width/10,height/4,str(100*positivity)+"% Positive");
    report.showPage();
    report.save();

def getCompanyName(ticker):
    yahoo = requests.get("http://d.yimg.com/autoc.finance.yahoo.com/autoc?query="+ticker+"&region=1&lang=en");
    yjson = yahoo.json();
    return yjson["ResultSet"]["Result"][0]["name"];



dji = ["MMM","AXP","AAPL","BA","CAT","CVX","CSCO","KK","DD","XM","GE"]

for i in ['DO']:
    genReport(i);
