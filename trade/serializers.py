from rest_framework import serializers

from sebi.models import Share
from . import models
from . import signals


class DeliverySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.DeliveryActivity
        fields = "__all__"


class DeliveryActivitySerializer(serializers.Serializer):

    quantity = serializers.IntegerField(required=True)
    price = serializers.FloatField(required=True)
    position = serializers.CharField(max_length=10, required=True)
    share = serializers.ModelField(model_field=Share()._meta.get_field('id'))

    def validate(self, data):
        user = self.context.get('request').user
        quantity = data.get('quantity')
        price = data.get('price')
        position = data.get('position')
        share = data.get('share')

        # check whether position is BUY or SELL
        if (position != "BUY" and position != "SELL"):
            msg = ('Position should be BUY or SELL')
            raise serializers.ValidationError(msg)   

        # check whether share is present in SEBI
        share_object = Share.objects.filter(id=share)
        if share_object:
            share_object = share_object.first()
        else:
            msg = ('Share not registered in local SEBI')
            raise serializers.ValidationError(msg)

        data = {
            "user": user, 
            "quantity": quantity, 
            "price": price, 
            "position": position, 
            "share": share_object
        }

        return data

    def create(self, validated_data):
        # create Delivery Activity
        instance = models.DeliveryActivity.objects.create(
            user=validated_data['user'], 
            share=validated_data['share'], 
            quantity=validated_data['quantity'], 
            price=validated_data['price'], 
            position=validated_data['position']
        )
        return instance


class IntradaySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Intraday
        fields = "__all__"


class IntradayActivitySerializer(serializers.Serializer):

    quantity = serializers.IntegerField(required=True)
    price = serializers.FloatField(required=True)
    position = serializers.CharField(max_length=10, required=True)
    share = serializers.ModelField(model_field=Share()._meta.get_field('id'))

    def validate(self, data):
        user = self.context.get('request').user
        quantity = data.get('quantity')
        price = data.get('price')
        position = data.get('position')
        share = data.get('share')

        # check whether position is BUY or SELL
        if (position != "BUY" and position != "SELL"):
            msg = ('Position should be BUY or SELL')
            raise serializers.ValidationError(msg)   

        # check whether share is present in SEBI
        share_object = Share.objects.filter(id=share)
        if share_object:
            share_object = share_object.first()
        else:
            msg = ('Share not registered in local SEBI')
            raise serializers.ValidationError(msg)

        data = {
            "user": user, 
            "quantity": quantity, 
            "price": price, 
            "position": position, 
            "share": share_object
        }

        return data

    def create(self, validated_data):
        # instantiate an object instance
        instance = models.IntradayActivity(
            user=validated_data['user'],
            share=validated_data['share'],
            quantity=validated_data['quantity'],
            price=validated_data['price'],
            position=validated_data['position']
        )

        signals.custom_intraday_activity_trade_signal.send(
            sender="IntradayActivitySerializer",
            request=self.context.get('request'),
            instance=instance    
        )
        # save the instance
        instance.save()
        return instance