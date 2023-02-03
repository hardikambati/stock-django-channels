from django.urls import path
from django.urls.conf import re_path
from . import consumers

# room_name
# stock_list : list of all stocks a user has requested
ws_urlpatterns = [
    path('ws/stock/<str:room_name>/<str:stock_list>/', consumers.StockConsumer.as_asgi()),
]