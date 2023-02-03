from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Avg
from django import dispatch

from rest_framework import status, exceptions

from . import models


custom_intraday_activity_trade_signal = dispatch.Signal(["request", "instance"])


@receiver(post_save, sender=models.DeliveryActivity)
def deliveryactivity_post_save(instance, **kwargs):
    if instance.position == "BUY":
        # check whether delivery object with reference to 
        # a user and a share exists
        delivery_instances = instance.user.delivery_set.filter(
            share=instance.share
        )

        if delivery_instances:
            delivery_object = delivery_instances.first()

            # fetch all delivery activities
            # calculate average price
            deliveryactivity_instances = instance.user.deliveryactivity_set.filter(
                share=instance.share
            )
            average_price = deliveryactivity_instances.aggregate(Avg('price'))
            delivery_object.quantity += instance.quantity
            delivery_object.average_price = average_price['price__avg']
            delivery_object.save()
        else:
            # create delivery object
            models.Delivery.objects.create(
                user=instance.user,
                share=instance.share, 
                quantity=instance.quantity,
                average_price=instance.price
            )

    elif instance.position == "SELL":
        # check whether delivery object with reference to 
        # a user and a share exists
        delivery_instances = instance.user.delivery_set.filter(
            user=instance.user, 
            share=instance.share
        )

        if delivery_instances:
            delivery_object = delivery_instances.first()

            quantity_left = delivery_object.quantity - instance.quantity
            if quantity_left == 0:
                delivery_object.delete()

            else:
                delivery_object.average_price = (
                    delivery_object.average_price * delivery_object.quantity - instance.price 
                ) / quantity_left * instance.quantity
                
                delivery_object.quantity -= instance.quantity
                delivery_object.save()
        else:
            raise exceptions.ValidationError({'detail': 'Position Invalid'})

    else:
        raise exceptions.ValidationError({'detail': 'Position Invalid'})


@dispatch.receiver(custom_intraday_activity_trade_signal)
def intraday_activity_trade_receiver(sender, request, instance, **kwargs):
    # if intraday_id is sent, manipulate existing stock
    # else create new instances

    existing_intraday_id = request.data.get('intraday_id', None)

    intraday_instances = instance.user.intraday_set.filter(
        share=instance.share,
        position=instance.position
    )

    if existing_intraday_id is not None and not '':
        existing_intraday_instances = models.Intraday.objects.filter(id=existing_intraday_id)
        if not existing_intraday_instances:
            raise exceptions.ValidationError(
                {'detail': 'Existing Intraday Instance not found'}
            )

        # buy the stocks which were sold (clear short position)
        # OR
        # sell the stocks which were bought (clear long position)
        existing_intraday_obj = existing_intraday_instances.first()
        if instance.quantity > existing_intraday_obj.quantity: 
            raise exceptions.ValidationError(
                    {'detail': 'Do not have enough shares'}
                )

        quantity_left = existing_intraday_obj.quantity - instance.quantity
        if quantity_left == 0:
            existing_intraday_obj.delete()    

        else:
            existing_intraday_obj.average_price = (
                existing_intraday_obj.average_price * existing_intraday_obj.quantity - instance.price*instance.quantity
            ) / quantity_left

            existing_intraday_obj.quantity -= instance.quantity
            existing_intraday_obj.save()

    elif intraday_instances:
        intraday_object = intraday_instances.first()

        # add to existing position if position is already open
        intradayactivity_instances = instance.user.intradayactivity_set.filter(
            share=instance.share,
            position=instance.position,
            is_active=True
        )

        average_price = intradayactivity_instances.aggregate(Avg('price'))
        intraday_object.quantity += instance.quantity
        intraday_object.average_price = average_price['price__avg']
        intraday_object.save()

    else:
        # create intraday object
        models.Intraday.objects.create(
            user=instance.user,
            share=instance.share,
            quantity=instance.quantity,
            position=instance.position,
            average_price=instance.price
        )
