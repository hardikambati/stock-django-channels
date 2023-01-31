from django.contrib import admin
from . import models

# Register your models here.

admin.site.register([
    models.Delivery,
    models.DeliveryActivity,
    models.Intraday,
    models.IntradayActivity,
])