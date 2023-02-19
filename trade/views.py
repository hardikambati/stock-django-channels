from django.shortcuts import render

from rest_framework import (permissions, status)
from rest_framework.views import APIView
from rest_framework.response import Response
            
from . import serializers
from utils import decorators

# create your views here.
# consists of all the transaction classes


class DeliveryView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        instance = request.user.delivery_set.all() 
        serializer = serializers.DeliverySerializer(
            instance, 
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK) 

    @decorators.shares_exists_before_sell
    def post(self, request, *args, **kwargs):
        serializer = serializers.DeliveryActivitySerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK) 


class IntradayView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        instance = request.user.intraday_set.all()

        serializer = serializers.IntradaySerializer(
            instance,
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        serializer = serializers.IntradayActivitySerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)