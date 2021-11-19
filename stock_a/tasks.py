from celery import shared_task, current_app, current_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import asyncio

# BEAT
from django_celery_beat.models import PeriodicTask, IntervalSchedule

# scraping
from urllib import request
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import yfinance as yf
import requests
from . import models


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


def calculate_percentage(price, change):

    price = price.replace(",", "")

    percent = (float(change)/float(price))*100

    return percent


@shared_task(bind=True)
def fetch_value(self, stocklist):

    # check whether there are users in the channel
    number_of_users = models.ChannelName.objects.count()

    if(number_of_users == 0):

        tasks = PeriodicTask.objects.filter(name="every-2-seconds")

        schedules = IntervalSchedule.objects.filter(every=5)

        if(len(tasks)>0):

            for i in tasks:

                i.delete()

        if(len(schedules)>0):

            for i in schedules:

                i.delete()

        print('Deleted tasks successfully')

        # current_app.control.revoke(current_task.request.id)

        # print(f'stopped task with id {current_task.request.id}')

    result = []
    for i in stocklist:

        try:
    
            filter_ticker = GOOGLE_FINANCE[i]

            request = requests.get('https://www.google.com/finance/quote/' + filter_ticker, headers={'User-Agent': 'Mozilla/5.0'})

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

            percent_price = "{:.2f}".format(calculate_percentage(current_price, change))

        except:

            current_price = ''

            previous_price = ''

        result.append({
            'company': i,
            'price': current_price,
            'change': change, 
            'percent': percent_price
        })    

    channel_layer = get_channel_layer()

    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)

    loop.run_until_complete(channel_layer.group_send('stock_stock_room', {
        'type': 'stock_update',
        'message': result
    }))
