from rest_framework import exceptions

from . import helpers
from trade.models import Delivery
from sebi.models import Share

# add wallet check balance
# does user have any shares to sell


def share_exists_in_sebi(func):
    """
    checks whether share exists in sebi
    """
    
    def check(*args, **kwargs):
        request = helpers.get_request(*args)

        shares = Share.objects.filter(id=request.data['share'])
        if shares:
            kwargs['share'] = shares.first()
            return func(*args, **kwargs)
        raise exceptions.ValidationError({'detail': 'Share not found in sebi'})
    return check


def shares_exists_before_sell(func):
    """
    checks whether
        - user has shares in Delivery table
    """

    @share_exists_in_sebi
    def check(*args, **kwargs):
        request = helpers.get_request(*args)

        if request.data['position'] == 'SELL':
            delivery_instances = Delivery.objects.filter(
                user=request.user,
                share=kwargs['share']
            )
            if not delivery_instances:
                raise exceptions.ValidationError({'detail': 'Please buy shares before selling'})
        
            # check for minimum shares
            if delivery_instances.first().quantity < request.data['quantity']:
                raise exceptions.ValidationError({'detail': 'Do not have enough shares to sell'})
        return func(*args, **kwargs)
    return check