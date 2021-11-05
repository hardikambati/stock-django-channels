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

            query_price, query_change, query_percent = query.call()

            inner_dict = {
                'name': i,
                'price': query_price,
                'change': query_change,
                'percent': query_percent
            }

            result.append(inner_dict)

        print('------ called ------')
        
        return Response(result)


class News(APIView):

    """
        fetch all news for NEWS page
    """

    def get(self, request):

        query = utility.NewsCall()

        news = query.call() 

        return Response(news)