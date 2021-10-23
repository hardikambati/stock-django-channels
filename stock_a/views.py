from django.shortcuts import render
from stock_a.utility import LiveCall, OHLCCall, StaticCall
from django.shortcuts import render, resolve_url
from . import utility

# rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


def driver(request):

    context = {
        'text': 'Hola Aliens'
    }

    return render(request, 'base.html', context)


class FetchStockData(APIView):

    def get(self, request):

        # data = request.data

        # ticker = data.get('ticker')

        # period = data.get('period')

        ticker = 'GOOG'
        
        if ticker is not None:

            try:

                ticker_cap = ticker.upper()
            
            except:

                ticker_cap = ticker

            try:
                api = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ ticker_cap +'&apikey=37VZLYPP251TU9OD')

                if(api.status_code==200):
                    json_val = json.loads(api.text)
                    json_next = json_val.get('Time Series (Daily)')

                    date = []
                    for i in json_next:
                        date.append(i)

                    open_v = []
                    high = []
                    low = []
                    close_v = []
                    for j in date[:16]:
                        value = json_next.get(j)
                        open_v.append(value.get('1. open'))
                        high.append(value.get('2. high'))
                        low.append(value.get('3. low'))
                        close_v.append(value.get('4. close'))

                    # all_data = zip(date, open_v, high, low, close_v)
                    return Response(close_v[0]) 

            except Exception as e:
                print(e)        
                return Response('failure') 

            return Response('success')

        else:

            return Response('NOTICKER')



class HistoryData(APIView):

    """
        fetch history data
        used yfinance library
    """
    
    def post(self, request):

        data = request.data

        ticker_arr = data['tickers']

        day = data.get('day', '1d')

        query = StaticCall(ticker_arr[0], day)

        query_res = query.call()

        return Response(query_res)



class OHLC(APIView):

    """
        fetch ohlc data for current date
    """

    def post(self, request):

        data = request.data

        print(data)

        ticker_arr = data['tickers']

        query = OHLCCall(ticker_arr[0])

        query_res = query.call()

        return Response(query_res)



class LiveData(APIView):

    """
        fetch live data
        if current time is between 9:00am - 3:40pm

        response format:

        result_dict = {
            {
                'name': 'INFY',
                'price': '1234', # current_value
                'change': '12'  # current_value - previous_close_value
            } 
        }

    """

    def post(self, request):

        data = request.data

        tickers = data['tickers']

        # tickers = ['INFY', 'RELIANCE', 'NIFTY']

        result = []

        for i in tickers:

            query = utility.LiveCall(i)

            query_price, query_change = query.call()

            inner_dict = {
                'name': i,
                'price': query_price,
                'change': query_change
            }

            result.append(inner_dict)

        print('------ called ------')
        
        return Response(result)
