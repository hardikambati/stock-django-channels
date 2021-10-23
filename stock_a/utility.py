from bs4 import BeautifulSoup
import requests
import yfinance as yf
import calendar


GOOGLE_FINANCE = {
    'SENSEX': 'SENSEX:INDEXBOM',
    'NIFTY': 'NIFTY_50:INDEXNSE',
    'INFY': 'INFY:NSE',
    'RELIANCE': 'RELIANCE:NSE',
    'HCLTECH': 'HCLTECH:NSE',
    'TATASTEEL': 'TATASTEEL:NSE',
    'HINDUSTANUNILEVER': 'HINDUNILVR:NSE',
    'TCS': 'TCS:NSE',
    'SBI': 'SBIN:NSE',
    'SUNPHARMA': 'SUNPHARMA:NSE'
}


YFINANCE = {
    'SENSEX': '^BSESN',
    'NIFTY': '^NSEI',
    'INFY': 'INFY.NS',
    'RELIANCE': 'RELIANCE.NS',
    'HCLTECH': 'HCLTECH.NS',
    'TATASTEEL': 'TATASTEEL.NS',
    'HINDUSTANUNILEVER': 'HINDUNILVR.NS',
    'TCS': 'TCS.NS',
    'SBI': 'SBIN.NS',
    'SUNPHARMA': 'SUNPHARMA.NS'
}


class LiveCall:

    def __init__(self, ticker):
        
        self.ticker = ticker

    
    def call(self):

        """
            return's 2 values
            current_price
            change
        """

        try:

            filter_ticker = GOOGLE_FINANCE[self.ticker]

            request = requests.get('https://www.google.com/finance/quote/' + filter_ticker, headers={'User-Agent': 'Mozilla/5.0'})
        
        except Exception as e:
        
            print(f'------- {e} -------')
        
            return '', ''

        soup = BeautifulSoup(request.content, features="html.parser")

        div_container_price = soup.find('div', {"class" : "YMlKec fxKbKc"})

        div_container_change = soup.find('div', {"class" : "P6K39c"})

        current_price = div_container_price.text

        previous_price = div_container_change.text
        

        if(current_price[0] == '₹'):

            current_price = current_price[1:]

        if(previous_price[0] == '₹'):

            previous_price = previous_price[1:]

        change_float = float(current_price.replace(",", "")) - float(previous_price.replace(",", ""))

        change = "{:.2f}".format(change_float)

        return current_price, change


class OHLCCall:

    def __init__(self, ticker):

        self.ticker = ticker

    
    def call(self):

        try:
            
            filter_ticker = YFINANCE[self.ticker]

            company = yf.Ticker(filter_ticker)

        except Exception as e:

            print(f'------- {e} -------')

            res_dict = {
                'Open': '0',
                'High': '0',
                'Low': '0',
                'Close': '0'
            }
            
            return res_dict


        hist = company.history(period="1d")

        tail = hist.tail(1)

        res_dict = {
            'Open': "{:.2f}".format(tail['Open'][0]),
            'High': "{:.2f}".format(tail['High'][0]),
            'Low': "{:.2f}".format(tail['Low'][0]),
            'Close': "{:.2f}".format(tail['Close'][0])
        }

        return res_dict


class StaticCall:

    def __init__(self, ticker, day=None):

        self.ticker = ticker
        self.day = day


    @staticmethod
    def filter_period(company, period):

        price = []
        date = []
        target = 1
        
        res = company.history(period)

        if(period == '5d'):

            for index, value in res.iterrows():

                date.append(str(index)[8:10])

                price.append(float("{:.2f}".format(value['Open'])))

            return date, price

        elif(period == '1mo'):

            target = 6

        elif(period == '3mo'):

            target = 3

        elif((period == '6mo') or (period == '1y') or (period == 'max')):

            target = 6

        for index, value in res.iterrows():

            if(period == '1mo'):
                month_number = str(index)[8:10]
                date.append(month_number)
            else:
                month_number = str(index)[5:7]
                date.append(calendar.month_name[int(month_number)][:3])

            price.append(float("{:.2f}".format(value['Open'])))

        date_div = len(date)//target

        new_date = []
        new_price = []

        for i in range(0, target):

            new_date.append(date[date_div*i])
            new_price.append(price[date_div*i])

        return new_date, new_price


    def call(self):

        """
            return's 2 arrays
            date: array of dates
            price: array of prices
        """

        price = []
        date = []

        try:
            
            filter_ticker = YFINANCE[self.ticker]

            company = yf.Ticker(filter_ticker)

        except Exception as e:

            print(f'------- {e} -------')

            return price, date

        if(self.day == '1d'):
        
            hist = yf.download(filter_ticker, period=self.day, interval="60m")
            
            for index, value in hist.iterrows():

                date.append(str(index)[11:16])

                price.append(float("{:.2f}".format(value['Open'])))

        else:

            date, price = self.filter_period(company, self.day)

        return date, price