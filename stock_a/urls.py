from django.urls import path
from . import views

urlpatterns = [
    path('', views.driver),
    
    path('fetch-history-data/', views.HistoryData.as_view()),
    path('fetch-ohlc-data/', views.OHLC.as_view()),
    path('fetch-live-data/', views.LiveData.as_view()),
]