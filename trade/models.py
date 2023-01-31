from django.db import models
from django.contrib.auth.models import User

from sebi.models import Share
from utils import helpers

# Create your models here.

POSITION_TYPES = (
    ("BUY", "BUY"),
    ("SELL", "SELL"),
)


class Delivery(models.Model):   # long term
    user = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE,
        blank=False
        
    )
    share = models.ForeignKey(
        to=Share, 
        on_delete=models.CASCADE,
        blank=False
    )
    quantity = models.IntegerField(blank=False)
    average_price = models.FloatField(blank=False)  # per share
    updated_on = models.DateTimeField(auto_now=True, blank=False)

    def __str__(self):
        return f'{self.user.username} : {self.share.name} : {self.quantity}' 


class Intraday(models.Model):   # one day
    user = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE,
        blank=False
        
    )
    share = models.ForeignKey(
        to=Share, 
        on_delete=models.CASCADE,
        blank=False
    )
    quantity = models.IntegerField(blank=False)
    position = models.CharField(max_length=10, choices=POSITION_TYPES, blank=False)
    average_price = models.FloatField(blank=False)  # per share
    valid_till = models.DateTimeField(default=helpers.add_custom_time_to_date())
    updated_on = models.DateTimeField(auto_now=True, blank=False)

    def __str__(self):
        return f'{self.user.username} : {self.share.name} : {self.quantity}' 


# TODO: add is_active field
class DeliveryActivity(models.Model):
    user = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE,
        blank=False
    )
    share = models.ForeignKey(
        to=Share, 
        on_delete=models.CASCADE,
        blank=False
    )
    quantity = models.IntegerField(blank=False)
    price = models.FloatField(blank=False)  # per share
    position = models.CharField(max_length=10, choices=POSITION_TYPES, blank=False)
    bought_on = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return self.share.name + ' : ' + self.position + ' : ' + str(self.quantity) 


class IntradayActivity(models.Model):
    user = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE,
        blank=False
        
    )
    share = models.ForeignKey(
        to=Share, 
        on_delete=models.CASCADE,
        blank=False
    )
    quantity = models.IntegerField(blank=False)
    price = models.FloatField(blank=False)  # per share
    is_active = models.BooleanField(default=True, blank=False)
    bought_on = models.DateTimeField(auto_now_add=True, blank=False)
    position = models.CharField(max_length=10, choices=POSITION_TYPES, blank=False)

    def __str__(self):
        return self.share.name + ' : ' + self.position + ' : ' + str(self.quantity) 