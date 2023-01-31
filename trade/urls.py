from django.urls import path
from . import views

urlpatterns = [
    path('delivery/', views.DeliveryView().as_view()),
    path('intraday/', views.IntradayView().as_view()),
]