# scraping
from urllib import request
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import yfinance as yf
import requests


def fetch_current_price():
    # NIFTY
    req = Request('https://www.moneycontrol.com/indian-indices/nifty-50-9.html', headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, features="html.parser")
    # price
    div_container = soup.find('div', {"class" : "inprice1"})
    ip_tag = div_container.find('input', {"id" : "spotValue"})
    
    return ip_tag['value']
