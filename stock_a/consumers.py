import asyncio
import json
from random import randint
from asyncio import sleep
from asgiref.sync import sync_to_async

from requests.models import Response
from channels.generic.websocket import AsyncWebsocketConsumer
from . import tasks
from . import models

# BEAT
from django_celery_beat.models import PeriodicTask, IntervalSchedule

# ROOM-GROUP-NAME: stock_stock_room

class StockConsumer(AsyncWebsocketConsumer):


    @sync_to_async
    def addToCeleryBeat(self, stocklist):

        task = PeriodicTask.objects.filter(name="every-10-seconds")

        if(len(task)>0):
            
            task = task.first()
            args = json.loads(task.args)
            args = args[0]
            
            # for x in stocklist:

            #     if x not in args:

            #         args.append(x)

            args = stocklist
            
            task.args = json.dumps([args])
            task.save()

        else:

            schedule, created = IntervalSchedule.objects.get_or_create(every=10, period=IntervalSchedule.SECONDS)

            task = PeriodicTask.objects.create(interval=schedule, name='every-10-seconds', task='stock_a.tasks.fetch_value', args=json.dumps([stocklist]))


    @sync_to_async
    def addToCustomRoom(self):
        room = models.Room.objects.all().first()
        
        # add to database
        models.ChannelName.objects.create(
            room_name = room,
            channel_name = self.channel_name
        )

    @sync_to_async
    def removeFromCustomRoom(self):

        target = models.ChannelName.objects.get(channel_name=self.channel_name)

        target.delete()


    @sync_to_async
    def get_watchlist(self):

        watchlist = models.Watchlist.objects.all()[0]

        watchlist_list = [stock.stock for stock in watchlist.stock.all()]   

        return watchlist_list


    async def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']

        # self.stock_list = self.scope['url_route']['kwargs']['stock_list']

        self.room_group_name = 'stock_%s' % self.room_name
        
        await self.addToCustomRoom()

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # stock_list = self.stock_list.split('-')
        print('----------------- connected ----------------')
        stock_list = await self.get_watchlist()

        await self.addToCeleryBeat(stock_list)

        await self.accept()

    
    async def disconnect(self, close_code):

        print('> disconnected ', self.room_group_name, self.channel_name)

        await self.removeFromCustomRoom()

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    # Receive message from WebSocket
    # async def receive(self, text_data):
    #     print('-------- receive function -----------')
    #     # text_data_json = json.loads(text_data)
    #     # print(text_data_json)
    #     # message = text_data_json['message']

    #     # Send message to room group
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             'type': 'stock_update',
    #             'message': text_data
    #         }
    #     )


    # Receive message from room group
    async def stock_update(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))

